Tests running `hg evolve` with in-memory merge.

  $ . $TESTDIR/testlib/common.sh

  $ cat >> $HGRCPATH <<EOF
  > [extensions]
  > evolve =
  > drawdag=$RUNTESTDIR/drawdag.py
  > [alias]
  > glog = log -G -T '{rev}:{node|short} {separate(" ", phase, tags)}\n{desc|firstline}'
  > [experimental]
  > evolution.in-memory = yes
  > EOF

Test evolving a single orphan

  $ hg init single-orphan
  $ cd single-orphan
  $ hg debugdrawdag <<'EOS'
  >     C  # C/c = c\n
  > B2  |  # B2/b = b2\n
  > |   B  # B/b = b\n
  >  \ /   # replace: B -> B2
  >   A
  > EOS
  1 new orphan changesets
  $ hg evolve
  move:[3] C
  atop:[2] B2
  $ hg glog
  o  4:52da76e91abb draft tip
  |  C
  | x  3:bc77848cde3a draft C
  | |  C
  o |  2:377a194b9b8a draft B2
  | |  B2
  | x  1:830b6315076c draft B
  |/   B
  o  0:426bada5c675 draft A
     A
  $ hg cat -r tip b c
  b2
  c
  $ cd ..

Test that in-memory evolve works when there are conflicts
and after continuing.

  $ hg init conflicts
  $ cd conflicts
  $ hg debugdrawdag <<'EOS'
  >     E  # E/e = e\n
  >     |
  >     D  # D/b = d\n
  >     |
  >     C  # C/c = c\n
  > B2  |  # B2/b = b2\n
  > |   B  # B/b = b\n
  >  \ /   # replace: B -> B2
  >   A
  > EOS
  3 new orphan changesets
  $ hg evolve
  move:[3] C
  atop:[2] B2
  move:[4] D
  merging b
  hit merge conflicts; retrying merge in working copy
  merging b
  warning: conflicts while merging b! (edit, then use 'hg resolve --mark')
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [240]
  $ hg glog
  @  6:52da76e91abb draft tip
  |  C
  | *  5:eae7899dd92b draft E
  | |  E
  | %  4:57e51f6a6d36 draft D
  | |  D
  | x  3:bc77848cde3a draft C
  | |  C
  o |  2:377a194b9b8a draft B2
  | |  B2
  | x  1:830b6315076c draft B
  |/   B
  o  0:426bada5c675 draft A
     A
  $ cat c
  c
  $ cat b
  <<<<<<< destination: 52da76e91abb - test: C
  b2
  =======
  d
  >>>>>>> evolving:    57e51f6a6d36 D - test: D
  $ echo d2 > b
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  evolving 4:57e51f6a6d36 "D"
  move:[5] E
  atop:[7] D
  $ hg glog
  o  8:3c658574f8ed draft tip
  |  E
  o  7:16e609b952e8 draft
  |  D
  o  6:52da76e91abb draft
  |  C
  | x  5:eae7899dd92b draft E
  | |  E
  | x  4:57e51f6a6d36 draft D
  | |  D
  | x  3:bc77848cde3a draft C
  | |  C
  o |  2:377a194b9b8a draft B2
  | |  B2
  | x  1:830b6315076c draft B
  |/   B
  o  0:426bada5c675 draft A
     A
  $ hg cat -r tip b c e
  d2
  c
  e
  $ cd ..

Test that in-memory merge is disabled if there's a precommit hook

  $ hg init precommit-hook
  $ cd precommit-hook
  $ hg debugdrawdag <<'EOS'
  >     C  # C/c = c\n
  > B2  |  # B2/b = b2\n
  > |   B  # B/b = b\n
  >  \ /   # replace: B -> B2
  >   A
  > EOS
  1 new orphan changesets
  $ cat >> .hg/hgrc <<EOF
  > [hooks]
  > precommit = echo "running precommit hook"
  > EOF
The hook is not run with in-memory=force
  $ hg co B2
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg evolve --config experimental.evolution.in-memory=force --update
  move:[3] C
  atop:[2] B2
  working directory is now at 52da76e91abb
  $ hg glog
  @  4:52da76e91abb draft tip
  |  C
  | x  3:bc77848cde3a draft C
  | |  C
  o |  2:377a194b9b8a draft B2
  | |  B2
  | x  1:830b6315076c draft B
  |/   B
  o  0:426bada5c675 draft A
     A
  $ hg co tip^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ hg amend -m B3
  1 new orphan changesets
The hook is run with in-memory=yes
  $ hg next --config experimental.evolution.in-memory=yes
  move:[4] C
  atop:[5] B3
  running precommit hook
  working directory is now at aeee7323c054
  $ hg glog
  @  6:aeee7323c054 draft tip
  |  C
  o  5:908ce5f9d7eb draft
  |  B3
  | x  3:bc77848cde3a draft C
  | |  C
  +---x  2:377a194b9b8a draft B2
  | |    B2
  | x  1:830b6315076c draft B
  |/   B
  o  0:426bada5c675 draft A
     A
