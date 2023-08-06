# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

"""
This file contains class to wrap the state for commands and other
related logic.

All the data related to the command state is stored as dictionary in the object.
The class has methods using which the data can be stored to disk in a file under
.hg/ directory.

We store the data on disk in cbor, for which we use cbor library to serialize
and deserialize data.
"""

from __future__ import absolute_import

import contextlib
import errno
import struct

from .thirdparty import cbor

from mercurial import (
    error,
    util,
)

from mercurial.i18n import _

class cmdstate(object):
    """a wrapper class to store the state of commands like `evolve`, `pick`

    All the data for the state is stored in the form of key-value pairs in a
    dictionary.

    The class object can write all the data to a file in .hg/ directory and also
    can populate the object data reading that file
    """

    def __init__(self, repo, path=b'evolvestate', opts=None):
        self._repo = repo
        self.path = path
        if opts is None:
            opts = {}
        self.opts = opts

    def __nonzero__(self):
        return self.exists()

    __bool__ = __nonzero__

    def __contains__(self, key):
        return key in self.opts

    def __getitem__(self, key):
        return self.opts[key]

    def get(self, key, default=None):
        return self.opts.get(key, default)

    def __setitem__(self, key, value):
        updates = {key: value}
        self.opts.update(updates)

    def load(self):
        """load the existing evolvestate file into the class object"""
        op = self._read()
        if isinstance(op, dict):
            self.opts.update(op)
        elif self.path == b'evolvestate':
            # it is the old evolvestate file
            oldop = _oldevolvestateread(self._repo)
            self.opts.update(oldop)

    def addopts(self, opts):
        """add more key-value pairs to the data stored by the object"""
        self.opts.update(opts)

    def save(self):
        """write all the evolvestate data stored in .hg/evolvestate file

        we use third-party library cbor to serialize data to write in the file.
        """
        with self._repo.vfs(self.path, b'wb', atomictemp=True) as fp:
            cbor.dump(self.opts, fp)

    def _read(self):
        """reads the evolvestate file and returns a dictionary which contain
        data in the same format as it was before storing"""
        with self._repo.vfs(self.path, b'rb') as fp:
            return cbor.load(fp)

    def delete(self):
        """drop the evolvestate file if exists"""
        util.unlinkpath(self._repo.vfs.join(self.path), ignoremissing=True)

    def exists(self):
        """check whether the evolvestate file exists or not"""
        return self._repo.vfs.exists(self.path)

def _oldevolvestateread(repo):
    """function to read the old evolvestate file

    This exists for BC reasons."""
    try:
        f = repo.vfs(b'evolvestate')
    except IOError as err:
        if err.errno != errno.ENOENT:
            raise
    try:
        versionblob = f.read(4)
        if len(versionblob) < 4:
            repo.ui.debug(b'ignoring corrupted evolvestate (file contains %i bits)\n'
                          % len(versionblob))
            return None
        version = struct.unpack(b'>I', versionblob)[0]
        if version != 0:
            msg = _(b'unknown evolvestate version %i') % version
            raise error.Abort(msg, hint=_(b'upgrade your evolve'))
        records = []
        data = f.read()
        off = 0
        end = len(data)
        while off < end:
            rtype = data[off]
            off += 1
            length = struct.unpack(b'>I', data[off:(off + 4)])[0]
            off += 4
            record = data[off:(off + length)]
            off += length
            if rtype == b't':
                rtype, record = record[0], record[1:]
            records.append((rtype, record))
        state = {}
        for rtype, rdata in records:
            if rtype == b'C':
                state[b'current'] = rdata
            elif rtype.lower():
                repo.ui.debug(b'ignore evolve state record type %s\n' % rtype)
            else:
                raise error.Abort(_(b"unknown evolvestate field type '%s'")
                                  % rtype, hint=_(b'upgrade your evolve'))
        return state
    finally:
        f.close()

@contextlib.contextmanager
def saver(state, opts=None):
    """ensure the state is saved on disk during the duration of the context

    The state is preserved if the context is exited through an exception.
    """
    if opts:
        state.addopts(opts)
    state.save()
    yield
    # delete only if no exception where raised
    state.delete()
