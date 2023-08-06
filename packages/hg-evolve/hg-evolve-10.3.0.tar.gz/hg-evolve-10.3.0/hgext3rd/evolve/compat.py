# Copyright 2017 Octobus <contact@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""
Compatibility module
"""

import array
import contextlib

from mercurial import (
    cmdutil,
    context,
    copies,
    hg,
    logcmdutil,
    merge as mergemod,
    obsolete,
    pycompat,
    registrar,
    repair,
    scmutil,
    util,
    ui as uimod,
)

if pycompat.ispy3:
    arraytobytes = array.array.tobytes
    arrayfrombytes = array.array.frombytes
else:
    arraytobytes = array.array.tostring
    arrayfrombytes = array.array.fromstring

# hg <= 5.2 (c21aca51b392)
try:
    from mercurial import pathutil
    dirs = pathutil.dirs
except (AttributeError, ImportError):
    dirs = util.dirs  # pytype: disable=module-attr

# hg <= 5.4 (b7808443ed6a)
try:
    from mercurial import mergestate as mergestatemod
    mergestate = mergestatemod.mergestate
except (AttributeError, ImportError):
    mergestate = mergemod.mergestate  # pytype: disable=module-attr

from . import (
    exthelper,
)

eh = exthelper.exthelper()

# Evolution renaming compat

TROUBLES = {
    r'ORPHAN': b'orphan',
    r'CONTENTDIVERGENT': b'content-divergent',
    r'PHASEDIVERGENT': b'phase-divergent',
}

# hg <= 4.6 (bec1212eceaa)
if util.safehasattr(uimod.ui, 'makeprogress'):
    def progress(ui, topic, pos, item=b"", unit=b"", total=None):
        progress = ui.makeprogress(topic, unit, total)
        if pos is not None:
            progress.update(pos, item=item)
        else:
            progress.complete()
else:
    def progress(ui, topic, pos, item=b"", unit=b"", total=None):
        ui.progress(topic, pos, item, unit, total)

# XXX: Better detection of property cache
if r'predecessors' not in dir(obsolete.obsstore):
    @property
    def predecessors(self):
        return self.precursors

    obsolete.obsstore.predecessors = predecessors

def memfilectx(repo, ctx, fctx, flags, copied, path):
    # XXX Would it be better at the module level?
    varnames = context.memfilectx.__init__.__code__.co_varnames  # pytype: disable=attribute-error

    if r"copysource" in varnames:
        mctx = context.memfilectx(repo, ctx, fctx.path(), fctx.data(),
                                  islink=b'l' in flags,
                                  isexec=b'x' in flags,
                                  copysource=copied.get(path))
    # hg <= 4.9 (550a172a603b)
    elif varnames[2] == r"changectx":
        mctx = context.memfilectx(repo, ctx, fctx.path(), fctx.data(),
                                  islink=b'l' in flags,
                                  isexec=b'x' in flags,
                                  copied=copied.get(path))  # pytype: disable=wrong-keyword-args
    return mctx

try:
    # hg <= 4.6 (46c2b19a1263)
    bmrevset = repair.stripbmrevset  # pytype: disable=module-attr
except AttributeError:
    bmrevset = scmutil.bookmarkrevs

hg48 = util.safehasattr(copies, 'stringutil')
# code imported from Mercurial core at ae17555ef93f + patch
def fixedcopytracing(repo, c1, c2, base):
    """A complete copy-patse of copies._fullcopytrace with a one line fix to
    handle when the base is not parent of both c1 and c2. This should be
    converted in a compat function once https://phab.mercurial-scm.org/D3896
    gets in and once we drop support for 4.6, this should be removed."""

    from mercurial import pathutil

    # In certain scenarios (e.g. graft, update or rebase), base can be
    # overridden We still need to know a real common ancestor in this case We
    # can't just compute _c1.ancestor(_c2) and compare it to ca, because there
    # can be multiple common ancestors, e.g. in case of bidmerge.  Because our
    # caller may not know if the revision passed in lieu of the CA is a genuine
    # common ancestor or not without explicitly checking it, it's better to
    # determine that here.
    #
    # base.isancestorof(wc) is False, work around that
    _c1 = c1.p1() if c1.rev() is None else c1
    _c2 = c2.p1() if c2.rev() is None else c2
    # an endpoint is "dirty" if it isn't a descendant of the merge base
    # if we have a dirty endpoint, we need to trigger graft logic, and also
    # keep track of which endpoint is dirty
    if util.safehasattr(base, 'isancestorof'):
        dirtyc1 = not base.isancestorof(_c1)
        dirtyc2 = not base.isancestorof(_c2)
    else: # hg <= 4.6 (fbec9c0b32d3)
        dirtyc1 = not base.descendant(_c1)
        dirtyc2 = not base.descendant(_c2)
    graft = dirtyc1 or dirtyc2
    tca = base
    if graft:
        tca = _c1.ancestor(_c2)

    # hg <= 4.9 (dc50121126ae)
    try:
        limit = copies._findlimit(repo, c1, c2)  # pytype: disable=module-attr
    except (AttributeError, TypeError):
        limit = copies._findlimit(repo, c1.rev(), c2.rev())  # pytype: disable=module-attr
    if limit is None:
        # no common ancestor, no copies
        return {}, {}, {}, {}, {}
    repo.ui.debug(b"  searching for copies back to rev %d\n" % limit)

    m1 = c1.manifest()
    m2 = c2.manifest()
    mb = base.manifest()

    # gather data from _checkcopies:
    # - diverge = record all diverges in this dict
    # - copy = record all non-divergent copies in this dict
    # - fullcopy = record all copies in this dict
    # - incomplete = record non-divergent partial copies here
    # - incompletediverge = record divergent partial copies here
    diverge = {} # divergence data is shared
    incompletediverge = {}
    data1 = {b'copy': {},
             b'fullcopy': {},
             b'incomplete': {},
             b'diverge': diverge,
             b'incompletediverge': incompletediverge,
             }
    data2 = {b'copy': {},
             b'fullcopy': {},
             b'incomplete': {},
             b'diverge': diverge,
             b'incompletediverge': incompletediverge,
             }

    # find interesting file sets from manifests
    if hg48:
        addedinm1 = m1.filesnotin(mb, repo.narrowmatch())
        addedinm2 = m2.filesnotin(mb, repo.narrowmatch())
    else:
        addedinm1 = m1.filesnotin(mb)
        addedinm2 = m2.filesnotin(mb)
    bothnew = sorted(addedinm1 & addedinm2)
    if tca == base:
        # unmatched file from base
        u1r, u2r = copies._computenonoverlap(repo, c1, c2, addedinm1, addedinm2)  # pytype: disable=module-attr
        u1u, u2u = u1r, u2r
    else:
        # unmatched file from base (DAG rotation in the graft case)
        u1r, u2r = copies._computenonoverlap(repo, c1, c2, addedinm1, addedinm2,  # pytype: disable=module-attr
                                             baselabel=b'base')
        # unmatched file from topological common ancestors (no DAG rotation)
        # need to recompute this for directory move handling when grafting
        mta = tca.manifest()
        if hg48:
            m1f = m1.filesnotin(mta, repo.narrowmatch())
            m2f = m2.filesnotin(mta, repo.narrowmatch())
            baselabel = b'topological common ancestor'
            u1u, u2u = copies._computenonoverlap(repo, c1, c2, m1f, m2f,  # pytype: disable=module-attr
                                                 baselabel=baselabel)
        else:
            u1u, u2u = copies._computenonoverlap(repo, c1, c2, m1.filesnotin(mta),  # pytype: disable=module-attr
                                                 m2.filesnotin(mta),
                                                 baselabel=b'topological common ancestor')

    for f in u1u:
        copies._checkcopies(c1, c2, f, base, tca, dirtyc1, limit, data1)  # pytype: disable=module-attr

    for f in u2u:
        copies._checkcopies(c2, c1, f, base, tca, dirtyc2, limit, data2)  # pytype: disable=module-attr

    copy = dict(data1[b'copy'])
    copy.update(data2[b'copy'])
    fullcopy = dict(data1[b'fullcopy'])
    fullcopy.update(data2[b'fullcopy'])

    if dirtyc1:
        copies._combinecopies(data2[b'incomplete'], data1[b'incomplete'], copy, diverge,  # pytype: disable=module-attr
                              incompletediverge)
    else:
        copies._combinecopies(data1[b'incomplete'], data2[b'incomplete'], copy, diverge,  # pytype: disable=module-attr
                              incompletediverge)

    renamedelete = {}
    renamedeleteset = set()
    divergeset = set()
    for of, fl in list(diverge.items()):
        if len(fl) == 1 or of in c1 or of in c2:
            del diverge[of] # not actually divergent, or not a rename
            if of not in c1 and of not in c2:
                # renamed on one side, deleted on the other side, but filter
                # out files that have been renamed and then deleted
                renamedelete[of] = [f for f in fl if f in c1 or f in c2]
                renamedeleteset.update(fl) # reverse map for below
        else:
            divergeset.update(fl) # reverse map for below

    if bothnew:
        repo.ui.debug(b"  unmatched files new in both:\n   %s\n"
                      % b"\n   ".join(bothnew))
    bothdiverge = {}
    bothincompletediverge = {}
    remainder = {}
    both1 = {b'copy': {},
             b'fullcopy': {},
             b'incomplete': {},
             b'diverge': bothdiverge,
             b'incompletediverge': bothincompletediverge
             }
    both2 = {b'copy': {},
             b'fullcopy': {},
             b'incomplete': {},
             b'diverge': bothdiverge,
             b'incompletediverge': bothincompletediverge
             }
    for f in bothnew:
        copies._checkcopies(c1, c2, f, base, tca, dirtyc1, limit, both1)  # pytype: disable=module-attr
        copies._checkcopies(c2, c1, f, base, tca, dirtyc2, limit, both2)  # pytype: disable=module-attr

    if dirtyc1 and dirtyc2:
        pass
    elif dirtyc1:
        # incomplete copies may only be found on the "dirty" side for bothnew
        assert not both2[b'incomplete']
        remainder = copies._combinecopies({}, both1[b'incomplete'], copy, bothdiverge,  # pytype: disable=module-attr
                                          bothincompletediverge)
    elif dirtyc2:
        assert not both1[b'incomplete']
        remainder = copies._combinecopies({}, both2[b'incomplete'], copy, bothdiverge,  # pytype: disable=module-attr
                                          bothincompletediverge)
    else:
        # incomplete copies and divergences can't happen outside grafts
        assert not both1[b'incomplete']
        assert not both2[b'incomplete']
        assert not bothincompletediverge
    for f in remainder:
        assert f not in bothdiverge
        ic = remainder[f]
        if ic[0] in (m1 if dirtyc1 else m2):
            # backed-out rename on one side, but watch out for deleted files
            bothdiverge[f] = ic
    for of, fl in bothdiverge.items():
        if len(fl) == 2 and fl[0] == fl[1]:
            copy[fl[0]] = of # not actually divergent, just matching renames

    if fullcopy and repo.ui.debugflag:
        repo.ui.debug(b"  all copies found (* = to merge, ! = divergent, "
                      b"% = renamed and deleted):\n")
        for f in sorted(fullcopy):
            note = b""
            if f in copy:
                note += b"*"
            if f in divergeset:
                note += b"!"
            if f in renamedeleteset:
                note += b"%"
            repo.ui.debug(b"   src: '%s' -> dst: '%s' %s\n" % (fullcopy[f], f,
                                                               note))
    del divergeset

    if not fullcopy:
        return copy, {}, diverge, renamedelete, {}

    repo.ui.debug(b"  checking for directory renames\n")

    # generate a directory move map
    d1, d2 = c1.dirs(), c2.dirs()
    # Hack for adding '', which is not otherwise added, to d1 and d2
    d1.addpath(b'/')
    d2.addpath(b'/')
    invalid = set()
    dirmove = {}

    # examine each file copy for a potential directory move, which is
    # when all the files in a directory are moved to a new directory
    for dst, src in fullcopy.items():
        dsrc, ddst = pathutil.dirname(src), pathutil.dirname(dst)
        if dsrc in invalid:
            # already seen to be uninteresting
            continue
        elif dsrc in d1 and ddst in d1:
            # directory wasn't entirely moved locally
            invalid.add(dsrc + b"/")
        elif dsrc in d2 and ddst in d2:
            # directory wasn't entirely moved remotely
            invalid.add(dsrc + b"/")
        elif dsrc + b"/" in dirmove and dirmove[dsrc + b"/"] != ddst + b"/":
            # files from the same directory moved to two different places
            invalid.add(dsrc + b"/")
        else:
            # looks good so far
            dirmove[dsrc + b"/"] = ddst + b"/"

    for i in invalid:
        if i in dirmove:
            del dirmove[i]
    del d1, d2, invalid

    if not dirmove:
        return copy, {}, diverge, renamedelete, {}

    for d in dirmove:
        repo.ui.debug(b"   discovered dir src: '%s' -> dst: '%s'\n" %
                      (d, dirmove[d]))

    movewithdir = {}
    # check unaccounted nonoverlapping files against directory moves
    for f in u1r + u2r:
        if f not in fullcopy:
            for d in dirmove:
                if f.startswith(d):
                    # new file added in a directory that was moved, move it
                    df = dirmove[d] + f[len(d):]
                    if df not in copy:
                        movewithdir[f] = df
                        repo.ui.debug((b"   pending file src: '%s' -> "
                                       b"dst: '%s'\n") % (f, df))
                    break

    return copy, movewithdir, diverge, renamedelete, dirmove

# hg <= 4.9 (7694b685bb10)
fixupstreamed = util.safehasattr(scmutil, 'movedirstate')
if not fixupstreamed:
    copies._fullcopytracing = fixedcopytracing

# help category compatibility
# hg <= 4.7 (c303d65d2e34)
def helpcategorykwargs(categoryname):
    """Backwards-compatible specification of the helpategory argument."""
    category = getattr(registrar.command, categoryname, None)
    if not category:
        return {}
    return {'helpcategory': category}

# nodemap.get and index.[has_node|rev|get_rev]
# hg <= 5.2 (02802fa87b74)
def getgetrev(cl):
    """Returns index.get_rev or nodemap.get (for pre-5.3 Mercurial)."""
    if util.safehasattr(cl.index, 'get_rev'):
        return cl.index.get_rev
    return cl.nodemap.get

@contextlib.contextmanager
def parentchange(repo):
    try:
        yield
    finally:
        # hg <= 5.2 (85c4cd73996b)
        if util.safehasattr(repo, '_quick_access_changeid_invalidate'):
            repo._quick_access_changeid_invalidate()

if util.safehasattr(mergemod, '_update'):
    def _update(*args, **kwargs):
        return mergemod._update(*args, **kwargs)
else:
    # hg <= 5.5 (2c86b9587740)
    def _update(*args, **kwargs):
        return mergemod.update(*args, **kwargs)

if (util.safehasattr(mergemod, '_update')
    and util.safehasattr(mergemod, 'update')):

    def update(ctx):
        mergemod.update(ctx)

    def clean_update(ctx):
        mergemod.clean_update(ctx)
else:
    # hg <= 5.5 (c1b603cdc95a)
    def update(ctx):
        hg.updaterepo(ctx.repo(), ctx.node(), overwrite=False)

    def clean_update(ctx):
        hg.updaterepo(ctx.repo(), ctx.node(), overwrite=True)

def cleanupnodes(repo, replacements, operation, moves=None, metadata=None):
    # Use this condition as a proxy since the commit we care about
    # (b99903534e06) didn't change any signatures.
    if util.safehasattr(scmutil, 'nullrev'):
        fixedreplacements = replacements
    else:
        # hg <= 4.7 (b99903534e06)
        fixedreplacements = {}
        for oldnodes, newnodes in replacements.items():
            for oldnode in oldnodes:
                fixedreplacements[oldnode] = newnodes

    scmutil.cleanupnodes(repo, replacements=fixedreplacements, operation=operation,
                         moves=moves, metadata=metadata)

if util.safehasattr(cmdutil, 'format_changeset_summary'):
    def format_changeset_summary_fn(ui, repo, command, default_spec):
        def show(ctx):
            text = cmdutil.format_changeset_summary(ui, ctx, command=command,
                                                    default_spec=default_spec)
            ui.write(b'%s\n' % text)
        return show
else:
    # hg <= 5.6 (96fcc37a9c80)
    def format_changeset_summary_fn(ui, repo, command, default_spec):
        return logcmdutil.changesetdisplayer(ui, repo,
                                             {b'template': default_spec}).show
