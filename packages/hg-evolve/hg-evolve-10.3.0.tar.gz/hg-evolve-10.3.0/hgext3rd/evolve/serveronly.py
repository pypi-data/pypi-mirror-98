'''enable experimental obsolescence feature of Mercurial

OBSOLESCENCE IS AN EXPERIMENTAL FEATURE MAKE SURE YOU UNDERSTOOD THE INVOLVED
CONCEPT BEFORE USING IT.

! THIS EXTENSION IS INTENDED FOR SERVER SIDE ONLY USAGE !

For client side usages it is recommended to use the evolve extension for
improved user interface.'''

from __future__ import absolute_import

import sys
import os

from mercurial import obsolete

try:
    from . import (
        compat,
        exthelper,
        metadata,
        obscache,
        obsexchange,
    )
except (ValueError, ImportError) as exc:
    if (isinstance(exc, ValueError)
        and str(exc) != b'Attempted relative import in non-package'):
        raise
    # extension imported using direct path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from evolve import (
        compat,
        exthelper,
        metadata,
        obscache,
        obsexchange,
    )

__version__ = metadata.__version__
testedwith = metadata.testedwith
minimumhgversion = metadata.minimumhgversion
buglink = metadata.buglink

eh = exthelper.exthelper()
eh.merge(compat.eh)
eh.merge(obscache.eh)
eh.merge(obsexchange.eh)
uisetup = eh.finaluisetup
extsetup = eh.finalextsetup
reposetup = eh.finalreposetup
cmdtable = eh.cmdtable
configtable = eh.configtable

@eh.reposetup
def default2evolution(ui, repo):
    evolveopts = repo.ui.configlist(b'experimental', b'evolution')
    if not evolveopts:
        evolveopts = b'all'
        repo.ui.setconfig(b'experimental', b'evolution', evolveopts, b'evolve')
    if obsolete.isenabled(repo, b'exchange'):
        # if no config explicitly set, disable bundle1
        if not isinstance(repo.ui.config(b'server', b'bundle1'), bytes):
            repo.ui.setconfig(b'server', b'bundle1', False, b'evolve')
