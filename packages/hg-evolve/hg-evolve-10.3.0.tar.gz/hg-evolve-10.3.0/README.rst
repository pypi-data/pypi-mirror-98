=============================
Mutable History For Mercurial
=============================

Evolve Extension
================

This package supplies the evolve extension for Mercurial,

**The full implementation of the changeset evolution concept is still in
progress.**  Please subscribe to the `evolve-testers mailing list
<https://www.mercurial-scm.org/mailman/listinfo/evolve-testers>`_ to stay up to
date with changes.

This extension:

* enables the "`changeset evolution`_" feature of core Mercurial,

* provides a set of commands to rewrite history in a distributed way,

* issues various warning messages when "troubles" from changeset evolution
  appear in your repository,

* provides an ``hg evolve`` command to deal with such troubles,

* improves performance of obsolescence marker exchange and discovery during
  push and pull.

.. _`changeset evolution`: https://www.mercurial-scm.org/wiki/ChangesetEvolution

Documentation
-------------

We recommend reading the documentation first. An online version is available
here:

    https://www.mercurial-scm.org/doc/evolution/

Source of the documentation can be found in ``docs/``.

How to Install
==============

Using Pip
---------

You can install the latest released version using pip::

    $ pip install --user hg-evolve

Then enable it in your hgrc::

    $ hg config --edit # add these two lines:
    [extensions]
    evolve =

From Source
-----------

To install a local version from source::

    $ hg clone https://www.mercurial-scm.org/repo/evolve/
    $ cd evolve
    # optionally `hg update <target revision>`
    $ pip install --user .

Then enable it in your hgrc::

    $ hg config --edit # add these two lines:
    [extensions]
    evolve =

It's also possible to use evolve without installing it, in which case you will
need to provide the full path to ``hgext3rd/evolve/``, for example::

    [extensions]
    evolve = ~/evolve/hgext3rd/evolve

Server-only Setup
=================

It is possible to enable a smaller subset of the features aimed at servers that
simply serve repositories::

    $ hg config --edit # add these two lines:
    [extensions]
    evolve.serveronly =

It skips the additions of the new commands and local UI messages that might add
performance overhead.

Extension Purpose
=================

The goal of this extension is to provide an appropriate place for code and
concepts related to `changeset evolution`_ to mature. In this extension we
allow hackier code, unlocking quick experimentation and faster iterations.

In addition, evolve extension supports a wide range of Mercurial versions,
allowing us to reach a larger user base for feedback. The extension is not tied
to the Mercurial release cycle and can release new features and bug fixes at a
higher rate if necessary.

Once a concept is deemed ready, its implementation is moved into core
Mercurial. The maturation period helped us to get a clearer picture of what was
needed. During the upstreaming process, we can use this clearer picture to
clean up the code and upgrade it to an appropriate quality for core Mercurial.

Python 3 Support
================

Mercurial announced official `support for Python 3`_ starting with its 5.2
release. Since 9.3.0, evolve has official support for Python 3.6+.

.. _`support for Python 3`: https://www.mercurial-scm.org/wiki/Python3

How to Contribute
=================

Discussion happens on the #hg-evolve IRC on freenode_.

.. _freenode: https://freenode.net/

Bugs are to be reported on the Mercurial's bug tracker (component:
`evolution`_).

.. _evolution: https://bz.mercurial-scm.org/buglist.cgi?component=evolution&query_format=advanced&resolution=---

The recommended way to submit a patch is to create a Merge Request on
https://foss.heptapod.net/mercurial/evolve. To do so, create an account and
request access. You'll then be able to create a topic-based merge request.

Alternatively, you can use the patchbomb extension to send email to `mercurial
devel <https://www.mercurial-scm.org/mailman/listinfo/mercurial-devel>`_.
Please make sure to use the evolve-ext flag when doing so. You can use a
command like this::

    $ hg email --to mercurial-devel@mercurial-scm.org --flag evolve-ext --rev '<your patches>'

For guidelines on the patch description, see the `official Mercurial guideline`_.

.. _`official Mercurial guideline`: https://mercurial-scm.org/wiki/ContributingChanges#Patch_descriptions

Please don't forget to update and run the tests when you fix a bug or add a
feature. To run the tests, you need a working copy of Mercurial, say in
$HGSRC::

    $ cd tests
    $ python $HGSRC/tests/run-tests.py

When certain blocks of code need to cope with API changes in core Mercurial,
they should have comments in the ``hg <= x.y (commit hash)`` format. For
example, if a function needs another code path because of changes introduced in
02802fa87b74 that was first included in Mercurial 5.3, then the comment should
be::

    # hg <= 5.2 (02802fa87b74)

See also tests/test-check-compat-strings.t.

Branch policy
-------------

The evolve tests are highly impacted by changes in core Mercurial. To deal with
this, we use named branches.

There are two main branches: "stable" and "default". Tests on these branches
are supposed to pass with the corresponding "default" and "stable" branch from
core Mercurial. The documentation is built from the tip of stable.

In addition, we have compatibility branches to check tests on older versions of
Mercurial. They are the "mercurial-x.y" branches. They are used to apply
expected test changes only, no code changes should happen there.

Test output changes from a changeset in core should add the following line to
their patch description::

    CORE-TEST-OUTPUT-UPDATE: <changeset hash>

Format-source config
====================

Format-source helps smooth out the pain of merging after auto-formatting.
Follow the installation instructions at the `format-source`_ repo.

.. _`format-source`: https://foss.heptapod.net/mercurial/format-source

Then update your per-repo config file::

    $ hg config --local --edit # add these lines:
    [extensions]
    formatsource =

    [format-source]
    byteify-strings = python3 ~/hg/contrib/byteify-strings.py --dictiter --treat-as-kwargs kwargs opts commitopts TROUBLES --allow-attr-methods
    byteify-strings:mode.input = file
    byteify-strings:mode.output = pipe

Release Checklist
=================

* make sure the tests are happy on all supported versions,

  You can use the `contrib/merge-test-compat.sh` to merge with the test
  compatibility branches.

* make sure there is no code difference between the compat branches and stable
  (no diff within `hgext3rd/`),

* update the `testedwith` variable for all extensions (remove '.dev'):

  - hgext3rd/evolve/metadata.py
  - hgext3rd/topic/__init__.py
  - hgext3rd/pullbundle.py

* make sure the changelog is up to date,

* add a date to the changelog entry for the target version,

* update the `__version__` field of all relevant extensions:

  - hgext3rd/evolve/metadata.py
  - hgext3rd/topic/__init__.py
  - hgext3rd/pullbundle.py (if touched)

* create a new Debian entry:

  - debchange --newversion x.y.z-1 "new upstream release"
  - debchange --release

* sanity check install and sdist targets of setup.py:

  - python setup.py install --home=$(mktemp -d)
  - python setup.py sdist

* tag the commit,

* push and publish the tag,

* upload the tarball to PyPI,

* make an announcement on evolve-testers@mercurial-scm.org (possibly on
  mercurial@mercurial-scm.org too),

* bump versions of all extensions and add '.dev' (see existing commits as an
  example):

  - hgext3rd/evolve/metadata.py
  - hgext3rd/topic/__init__.py
  - hgext3rd/pullbundle.py

  The version we use on the stable branch during development should be
  `x.y.z+1.dev`. The version of the default branch should be `x.y+1.0.dev`.

* merge stable into default.
