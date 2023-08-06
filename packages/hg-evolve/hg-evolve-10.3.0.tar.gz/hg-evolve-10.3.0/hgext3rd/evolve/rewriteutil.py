# Module dedicated to host utility code dedicated to changeset rewrite
#
# Copyright 2017 Octobus <contact@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

# Status: Stabilization of the API in progress
#
#   The content of this module should move into core incrementally once we are
#   happy one piece of it (and hopefully, able to reuse it in other core
#   commands).

from mercurial import (
    cmdutil,
    commands,
    context,
    copies,
    error,
    hg,
    lock as lockmod,
    node,
    obsolete,
    obsutil,
    revset,
    util,
)

from mercurial.i18n import _

from . import (
    compat,
)

def _formatrevs(repo, revs, maxrevs=4):
    """return a string summarising revision in a descent size

    If there is few enough revision, we list them otherwise we display a
    summary in the form:

        1ea73414a91b and 5 others
    """
    tonode = repo.changelog.node
    numrevs = len(revs)
    if numrevs < maxrevs:
        shorts = [node.short(tonode(r)) for r in revs]
        summary = b', '.join(shorts)
    else:
        first = revs.first()
        summary = _(b'%s and %d others')
        summary %= (node.short(tonode(first)), numrevs - 1)
    return summary

def precheck(repo, revs, action=b'rewrite'):
    """check if <revs> can be rewritten

    <action> can be used to control the commit message.
    """
    if node.nullrev in revs:
        msg = _(b"cannot %s the null revision") % (action)
        hint = _(b"no changeset checked out")
        raise error.Abort(msg, hint=hint)
    if any(util.safehasattr(r, 'rev') for r in revs):
        msg = b"rewriteutil.precheck called with ctx not revs"
        repo.ui.develwarn(msg)
        revs = (r.rev() for r in revs)
    publicrevs = repo.revs(b'%ld and public()', revs)
    if publicrevs:
        summary = _formatrevs(repo, publicrevs)
        msg = _(b"cannot %s public changesets: %s") % (action, summary)
        hint = _(b"see 'hg help phases' for details")
        raise error.Abort(msg, hint=hint)
    newunstable = disallowednewunstable(repo, revs)
    if newunstable:
        msg = _(b"%s will orphan %i descendants")
        msg %= (action, len(newunstable))
        hint = _(b"see 'hg help evolution.instability'")
        raise error.Abort(msg, hint=hint)
    divrisk = revs_hascontentdivrisk(repo, revs)
    allowdivergence = repo.ui.configbool(b'experimental',
                                         b'evolution.allowdivergence')
    if divrisk and not allowdivergence:
        localdiv = repo[divrisk[0]]
        otherdiv, base = repo[divrisk[1][0]], repo[divrisk[1][1]]
        msg = _(b"%s of %s creates content-divergence "
                b"with %s") % (action, localdiv, otherdiv)
        if localdiv.rev() != base.rev():
            msg += _(b', from %s') % base
        hint = _(b"add --verbose for details or see "
                 b"'hg help evolution.instability'")
        if repo.ui.verbose:
            if localdiv.rev() != base.rev():
                msg += _(b'\n    changeset %s is an evolution of '
                         b'changeset %s') % (localdiv, base)
            msg += _(b'\n    changeset %s already have a successors as '
                     b'changeset %s\n'
                     b'    rewriting changeset %s would create '
                     b'"content-divergence"\n'
                     b'    set experimental.evolution.allowdivergence=True to '
                     b'overwrite this check') % (base, otherdiv, localdiv)
            hint = _(b"see 'hg help evolution.instability' for details "
                     b"on content-divergence")
        raise error.Abort(msg, hint=hint)

def bookmarksupdater(repo, oldid, tr):
    """Return a callable update(newid) updating the current bookmark
    and bookmarks bound to oldid to newid.
    """
    def updatebookmarks(newid):
        oldbookmarks = repo.nodebookmarks(oldid)
        bmchanges = [(b, newid) for b in oldbookmarks]
        if bmchanges:
            repo._bookmarks.applychanges(repo, tr, bmchanges)
    return updatebookmarks

def revs_hascontentdivrisk(repo, revs):
    obsrevs = repo.revs(b'%ld and obsolete()', revs)
    for r in obsrevs:
        div = precheck_contentdiv(repo, repo[r])
        if div:
            return [r, div]
    return []

def disallowednewunstable(repo, revs):
    """Check that editing <revs> will not create disallowed unstable

    (unstable creation is controled by some special config).
    """
    allowunstable = obsolete.isenabled(repo, obsolete.allowunstableopt)
    if allowunstable:
        return revset.baseset()
    return repo.revs(b"(%ld::) - %ld", revs, revs)

def foldcheck(repo, revs):
    """check that <revs> can be folded"""
    precheck(repo, revs, action=b'fold')
    roots = repo.revs(b'roots(%ld)', revs)
    if len(roots) > 1:
        raise error.Abort(_(b"cannot fold non-linear revisions "
                            b"(multiple roots given)"))
    heads = repo.revs(b'heads(%ld)', revs)
    if len(heads) > 1:
        raise error.Abort(_(b"cannot fold non-linear revisions "
                            b"(multiple heads given)"))
    head = repo[heads.first()]
    baseparents = repo.revs(b'parents(%ld) - %ld', revs, revs)
    if len(baseparents) > 2:
        raise error.Abort(_(b"cannot fold revisions that merge with more than "
                            b"one external changeset (not in revisions)"))
    if not repo.ui.configbool(b'experimental', b'evolution.allowdivergence'):
        obsolete = repo.revs(b'%ld and obsolete()', revs)
        if obsolete:
            msg = _(b'folding obsolete revisions may cause divergence')
            hint = _(b'set experimental.evolution.allowdivergence=yes'
                     b' to allow folding them')
            raise error.Abort(msg, hint=hint)
    root = repo[roots.first()]
    # root's p1 is already used as the target ctx p1
    baseparents -= {root.p1().rev()}
    p2 = repo[baseparents.first()]
    return root, head, p2

def deletebookmark(repo, repomarks, bookmarks):
    wlock = lock = tr = None
    try:
        wlock = repo.wlock()
        lock = repo.lock()
        tr = repo.transaction(b'prune')
        bmchanges = []
        for bookmark in bookmarks:
            bmchanges.append((bookmark, None))
        repo._bookmarks.applychanges(repo, tr, bmchanges)
        tr.close()
        for bookmark in sorted(bookmarks):
            repo.ui.write(_(b"bookmark '%s' deleted\n") % bookmark)
    finally:
        lockmod.release(tr, lock, wlock)

def presplitupdate(repo, ui, prev, ctx):
    """prepare the working directory for a split (for topic hooking)
    """
    hg.update(repo, prev)
    commands.revert(ui, repo, rev=ctx.hex(), all=True)

def reachablefrombookmark(repo, revs, bookmarks):
    """filter revisions and bookmarks reachable from the given bookmark
    yoinked from mq.py
    """
    repomarks = repo._bookmarks
    if not bookmarks.issubset(repomarks):
        raise error.Abort(_(b"bookmark '%s' not found") %
                          b','.join(sorted(bookmarks - set(repomarks.keys()))))

    # If the requested bookmark is not the only one pointing to a
    # a revision we have to only delete the bookmark and not strip
    # anything. revsets cannot detect that case.
    nodetobookmarks = {}
    for mark, bnode in repomarks.items():
        nodetobookmarks.setdefault(bnode, []).append(mark)
    for marks in nodetobookmarks.values():
        if bookmarks.issuperset(marks):
            rsrevs = compat.bmrevset(repo, marks[0])
            revs = set(revs)
            revs.update(set(rsrevs))
            revs = sorted(revs)
    return repomarks, revs

def rewrite(repo, old, updates, head, newbases, commitopts):
    """Return (nodeid, created) where nodeid is the identifier of the
    changeset generated by the rewrite process, and created is True if
    nodeid was actually created. If created is False, nodeid
    references a changeset existing before the rewrite call.
    """
    wlock = lock = tr = None
    try:
        wlock = repo.wlock()
        lock = repo.lock()
        tr = repo.transaction(b'rewrite')
        base = old.p1()
        updatebookmarks = bookmarksupdater(repo, old.node(), tr)

        # commit a new version of the old changeset, including the update
        # collect all files which might be affected
        files = set(old.files())
        for u in updates:
            files.update(u.files())

        # Recompute copies (avoid recording a -> b -> a)
        copied = copies.pathcopies(base, head)

        # prune files which were reverted by the updates
        def samefile(f):
            if f in head.manifest():
                a = head.filectx(f)
                if f in base.manifest():
                    b = base.filectx(f)
                    return (a.data() == b.data()
                            and a.flags() == b.flags())
                else:
                    return False
            else:
                return f not in base.manifest()
        files = [f for f in files if not samefile(f)]
        # commit version of these files as defined by head
        headmf = head.manifest()

        def filectxfn(repo, ctx, path):
            if path in headmf:
                fctx = head[path]
                flags = fctx.flags()
                mctx = compat.memfilectx(repo, ctx, fctx, flags, copied, path)
                return mctx
            return None

        message = cmdutil.logmessage(repo.ui, commitopts)
        if not message:
            message = old.description()

        user = commitopts.get(b'user') or old.user()
        # TODO: In case not date is given, we should take the old commit date
        # if we are working one one changeset or mimic the fold behavior about
        # date
        date = commitopts.get(b'date') or None
        extra = dict(commitopts.get(b'extra', old.extra()))
        extra[b'branch'] = head.branch()

        new = context.memctx(repo,
                             parents=newbases,
                             text=message,
                             files=files,
                             filectxfn=filectxfn,
                             user=user,
                             date=date,
                             extra=extra)

        if commitopts.get(b'edit'):
            new._text = cmdutil.commitforceeditor(repo, new, [])
        revcount = len(repo)
        newid = repo.commitctx(new)
        new = repo[newid]
        created = len(repo) != revcount
        updatebookmarks(newid)

        tr.close()
        return newid, created
    finally:
        lockmod.release(tr, lock, wlock)

def precheck_contentdiv(repo, ctx):
    """return divergent revision if rewriting an obsolete cset (ctx) will
    create divergence"""
    # We need to check two cases that can cause divergence:
    # case 1: the rev being rewritten has a non-obsolete successor (easily
    #     detected by successorssets)
    divergent = [] # contains [divergent_cset, common_precursor]
    sset = obsutil.successorssets(repo, ctx.node())
    nodivergencerisk = (len(sset) == 0
                        or (len(sset) == 1
                            and len(sset[0]) == 1
                            and repo[sset[0][0]].rev() == ctx.rev()
                        ))
    if nodivergencerisk:
        # case 2: one of the precursors of the rev being revived has a
        #     non-obsolete successor (we need divergentsets for this)
        from . import evolvecmd
        divsets = evolvecmd.divergentsets(repo, ctx)
        if divsets:
            nsuccset = divsets[0][b'divergentnodes']
            divergent.append(nsuccset[0])
            prec = divsets[0][b'commonprecursor']
            divergent.append(prec)
    else:
        divergent.append(sset[0][0])
        divergent.append(ctx.node())
    return divergent
