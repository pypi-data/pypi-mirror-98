from __future__ import absolute_import

import collections
import contextlib
import weakref

from mercurial.i18n import _
from mercurial import (
    bundle2,
    discovery,
    error,
    exchange,
    extensions,
    scmutil,
    util,
)
from . import (
    common,
    compat,
)

from mercurial import wireprotov1server

@contextlib.contextmanager
def override_context_branch(repo, publishedset=()):
    unfi = repo.unfiltered()

    class repocls(unfi.__class__):
        # awful hack to see branch as "branch:topic"
        def __getitem__(self, key):
            ctx = super(repocls, self).__getitem__(key)
            oldbranch = ctx.branch
            oldparents = ctx.parents
            rev = ctx.rev()

            def branch():
                branch = oldbranch()
                if rev in publishedset:
                    return branch
                topic = ctx.topic()
                if topic:
                    branch = b"%s:%s" % (branch, topic)
                return branch

            def parents():
                parents = oldparents()
                for p in parents:
                    if getattr(p, '_topic_ext_branch_hack', False):
                        continue
                    pbranch = p.branch

                    def branch():
                        branch = pbranch()
                        if p.rev() in publishedset:
                            return branch
                        topic = p.topic()
                        if topic:
                            branch = b"%s:%s" % (branch, topic)
                        return branch
                    p.branch = branch
                    p._topic_ext_branch_hack = True
                return parents

            ctx.branch = branch
            ctx.parents = parents
            return ctx

        def revbranchcache(self):
            rbc = super(repocls, self).revbranchcache()
            localchangelog = self.changelog

            def branchinfo(rev, changelog=None):
                if changelog is None:
                    changelog = localchangelog
                branch, close = changelog.branchinfo(rev)
                if rev in publishedset:
                    return branch, close
                topic = unfi[rev].topic()
                if topic:
                    branch = b"%s:%s" % (branch, topic)
                return branch, close

            rbc.branchinfo = branchinfo
            return rbc

    oldrepocls = unfi.__class__
    try:
        unfi.__class__ = repocls
        if repo.filtername is not None:
            repo = unfi.filtered(repo.filtername)
        else:
            repo = unfi
        yield repo
    finally:
        unfi.__class__ = oldrepocls


def _headssummary(orig, pushop, *args, **kwargs):
    repo = pushop.repo.unfiltered()
    remote = pushop.remote

    publishing = (b'phases' not in remote.listkeys(b'namespaces')
                  or bool(remote.listkeys(b'phases').get(b'publishing', False)))

    if not common.hastopicext(pushop.repo):
        return orig(pushop, *args, **kwargs)
    elif ((publishing or not remote.capable(b'topics'))
            and not getattr(pushop, 'publish', False)):
        return orig(pushop, *args, **kwargs)

    publishedset = ()
    remotebranchmap = None
    origremotebranchmap = remote.branchmap
    publishednode = [c.node() for c in pushop.outdatedphases]
    publishedset = repo.revs(b'ancestors(%ln + %ln)',
                             publishednode,
                             pushop.remotephases.publicheads)

    getrev = compat.getgetrev(repo.unfiltered().changelog)

    def remotebranchmap():
        # drop topic information from changeset about to be published
        result = collections.defaultdict(list)
        for branch, heads in compat.branchmapitems(origremotebranchmap()):
            if b':' not in branch:
                result[branch].extend(heads)
            else:
                namedbranch = branch.split(b':', 1)[0]
                for h in heads:
                    r = getrev(h)
                    if r is not None and r in publishedset:
                        result[namedbranch].append(h)
                    else:
                        result[branch].append(h)
        for heads in result.values():
            heads.sort()
        return result

    with override_context_branch(repo, publishedset=publishedset):
        try:
            if remotebranchmap is not None:
                remote.branchmap = remotebranchmap
            unxx = repo.filtered(b'unfiltered-topic')
            repo.unfiltered = lambda: unxx
            pushop.repo = repo
            summary = orig(pushop)
            for key, value in summary.items():
                if b':' in key: # This is a topic
                    if value[0] is None and value[1]:
                        summary[key] = ([value[1][0]], ) + value[1:]
            return summary
        finally:
            if r'unfiltered' in vars(repo):
                del repo.unfiltered
            if remotebranchmap is not None:
                remote.branchmap = origremotebranchmap

def wireprotobranchmap(orig, repo, proto):
    if not common.hastopicext(repo):
        return orig(repo, proto)
    oldrepo = repo.__class__
    try:
        class repocls(repo.__class__):
            def branchmap(self):
                usetopic = not self.publishing()
                return super(repocls, self).branchmap(topic=usetopic)
        repo.__class__ = repocls
        return orig(repo, proto)
    finally:
        repo.__class__ = oldrepo


def _get_branch_name(ctx):
    # make it easy for extension with the branch logic there
    return ctx.branch()


def _filter_obsolete_heads(repo, heads):
    """filter heads to return non-obsolete ones

    Given a list of heads (on the same named branch) return a new list of heads
    where the obsolete part have been skimmed out.
    """
    new_heads = []
    old_heads = heads[:]
    while old_heads:
        rh = old_heads.pop()
        ctx = repo[rh]
        current_name = _get_branch_name(ctx)
        # run this check early to skip the evaluation of the whole branch
        if not ctx.obsolete():
            new_heads.append(rh)
            continue

        # Get all revs/nodes on the branch exclusive to this head
        # (already filtered heads are "ignored"))
        sections_revs = repo.revs(
            b'only(%d, (%ld+%ld))', rh, old_heads, new_heads,
        )
        keep_revs = []
        for r in sections_revs:
            ctx = repo[r]
            if ctx.obsolete():
                continue
            if _get_branch_name(ctx) != current_name:
                continue
            keep_revs.append(r)
        for h in repo.revs(b'heads(%ld and (::%ld))', sections_revs, keep_revs):
            new_heads.append(h)
    new_heads.sort()
    return new_heads

# Discovery have deficiency around phases, branch can get new heads with pure
# phases change. This happened with a changeset was allowed to be pushed
# because it had a topic, but it later become public and create a new branch
# head.
#
# Handle this by doing an extra check for new head creation server side
def _nbheads(repo):
    data = {}
    for b in repo.branchmap().iterbranches():
        if b':' in b[0]:
            continue
        oldheads = [repo[n].rev() for n in b[1]]
        newheads = _filter_obsolete_heads(repo, oldheads)
        data[b[0]] = newheads
    return data

def handlecheckheads(orig, op, inpart):
    """This is used to check for new heads when publishing changeset"""
    orig(op, inpart)
    if not common.hastopicext(op.repo) or op.repo.publishing():
        return
    tr = op.gettransaction()
    if tr.hookargs[b'source'] not in (b'push', b'serve'): # not a push
        return
    tr._prepushheads = _nbheads(op.repo)
    reporef = weakref.ref(op.repo)
    if util.safehasattr(tr, 'validator'): # hg <= 4.7 (ebbba3ba3f66)
        oldvalidator = tr.validator
    elif util.safehasattr(tr, '_validator'):
        # hg <= 5.3 (36f08ae87ef6)
        oldvalidator = tr._validator

    def _validate(tr):
        repo = reporef()
        if repo is not None:
            repo.invalidatecaches()
            finalheads = _nbheads(repo)
            for branch, oldnb in tr._prepushheads.items():
                newheads = finalheads.pop(branch, [])
                if len(oldnb) < len(newheads):
                    cl = repo.changelog
                    newheads = sorted(set(newheads).difference(oldnb))
                    heads = scmutil.nodesummaries(repo, [cl.node(r) for r in newheads])
                    msg = _(
                        b"push creates new heads on branch '%s': %s"
                        % (branch, heads)
                    )
                    raise error.Abort(msg)
            for branch, newnb in finalheads.items():
                if 1 < len(newnb):
                    cl = repo.changelog
                    heads = scmutil.nodesummaries(repo, [cl.node(r) for r in newnb])
                    msg = _(
                        b"push creates new branch '%s' with multiple heads: %s"
                        % (branch, heads)
                    )
                    hint = _(b"merge or see 'hg help push' for details about "
                             b"pushing new heads")
                    raise error.Abort(msg, hint=hint)

    def validator(tr):
        _validate(tr)
        return oldvalidator(tr)

    if util.safehasattr(tr, 'validator'): # hg <= 4.7 (ebbba3ba3f66)
        tr.validator = validator
    elif util.safehasattr(tr, '_validator'):
        # hg <= 5.3 (36f08ae87ef6)
        tr._validator = validator
    else:
        tr.addvalidator(b'000-new-head-check', _validate)

handlecheckheads.params = frozenset()

def _pushb2phases(orig, pushop, bundler):
    if common.hastopicext(pushop.repo):
        checktypes = (b'check:heads', b'check:updated-heads')
        hascheck = any(p.type in checktypes for p in bundler._parts)
        if not hascheck and pushop.outdatedphases:
            exchange._pushb2ctxcheckheads(pushop, bundler)
    return orig(pushop, bundler)

def wireprotocaps(orig, repo, proto):
    caps = orig(repo, proto)
    if common.hastopicext(repo) and repo.peer().capable(b'topics'):
        caps.append(b'topics')
    return caps

def modsetup(ui):
    """run at uisetup time to install all destinations wrapping"""
    extensions.wrapfunction(discovery, '_headssummary', _headssummary)
    extensions.wrapfunction(wireprotov1server, 'branchmap', wireprotobranchmap)
    extensions.wrapfunction(wireprotov1server, '_capabilities', wireprotocaps)
    # we need a proper wrap b2 part stuff
    extensions.wrapfunction(bundle2, 'handlecheckheads', handlecheckheads)
    bundle2.handlecheckheads.params = frozenset()
    bundle2.parthandlermapping[b'check:heads'] = bundle2.handlecheckheads
    if util.safehasattr(bundle2, 'handlecheckupdatedheads'):
        # we still need a proper wrap b2 part stuff
        extensions.wrapfunction(bundle2, 'handlecheckupdatedheads', handlecheckheads)
        bundle2.handlecheckupdatedheads.params = frozenset()
        bundle2.parthandlermapping[b'check:updated-heads'] = bundle2.handlecheckupdatedheads
    extensions.wrapfunction(exchange, '_pushb2phases', _pushb2phases)
    exchange.b2partsgenmapping[b'phase'] = exchange._pushb2phases
