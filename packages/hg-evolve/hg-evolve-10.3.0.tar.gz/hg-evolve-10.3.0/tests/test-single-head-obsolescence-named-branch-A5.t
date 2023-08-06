=========================================
Testing single head enforcement: Case A-1
=========================================

A repository is set to only accept a single head per name (typically named
branch). However, obsolete changesets can make this enforcement more
complicated, because they can be kept visible by other changeset on other
branch.

This case is part of a series of tests checking this behavior.

Category A: Involving obsolescence
TestCase 1: obsoleting a merge reveal two heads

.. old-state:
..
.. * 3 changeset changeset on branch default (2 on their own branch + 1 merge)
.. * 1 changeset on branch Z (children of the merge)
..
.. new-state:
..
.. * 2 changeset changeset on branch default (merge is obsolete) each a head
.. * 1 changeset on branch Z keeping the merge visible
..
.. expected-result:
..
.. * 2 heads detected (because we skip the merge).
..
.. graph-summary:
..
..   D ●      (branch Z)
..     |
..   C ●      (branch Z)
..     |
..   M ⊗
..     |\
..   A ● ● B
..     |/
..     ●

  $ . $TESTDIR/testlib/topic_setup.sh
  $ . $TESTDIR/testlib/push-checkheads-util.sh

Test setup
----------

  $ mkdir A5
  $ cd A5
  $ setuprepos single-head
  creating basic server and client repo
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd client
  $ hg up 0
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit B0
  created new head
  (consider using topic for lightweight branches. See 'hg help topic')
  $ hg merge
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m 'M0'
  $ hg branch Z
  marked working directory as branch Z
  (branches are permanent and global, did you want a bookmark?)
  $ mkcommit C0
  $ hg push --new-branch
  pushing to $TESTTMP/A5/server
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 3 changesets with 2 changes to 2 files
  $ hg up 0
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ mkcommit A1
  created new head
  (consider using topic for lightweight branches. See 'hg help topic')
  $ mkcommit B1
  $ hg debugobsolete `getid "desc(M0)"` --record-parents
  1 new obsolescence markers
  obsoleted 1 changesets
  1 new orphan changesets
  $ hg log -G --hidden
  @  262c8c798096 [default] (draft): B1
  |
  o  f6082bc4ffef [default] (draft): A1
  |
  | *  61c95483cc12 [Z] (draft): C0
  | |
  | x    14d3d4d41d1a [default] (draft): M0
  | |\
  +---o  74ff5441d343 [default] (draft): B0
  | |
  | o  8aaa48160adc [default] (draft): A0
  |/
  o  1e4be0697311 [default] (public): root
  

Actual testing
--------------

(force push to make sure we get the changeset on the remote)

  $ hg push -r 'desc("C0")' --force
  pushing to $TESTTMP/A5/server
  searching for changes
  no changes found
  transaction abort!
  rollback completed
  abort: rejecting multiple heads on branch "default"
  (2 heads: 8aaa48160adc 74ff5441d343)
  [255]
