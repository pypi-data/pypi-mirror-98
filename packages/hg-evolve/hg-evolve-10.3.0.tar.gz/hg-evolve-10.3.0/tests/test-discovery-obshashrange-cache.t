==============================
Test cache warming strategy 
test for range based discovery
==============================

  $ . $TESTDIR/testlib/pythonpath.sh

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > hgext3rd.evolve =
  > blackbox =
  > [defaults]
  > blackbox = -l 100
  > [experimental]
  > obshashrange=1
  > verbose-obsolescence-exchange=1
  > [ui]
  > logtemplate = "{rev} {node|short} {desc} {tags}\n"
  > ssh = "$PYTHON" "$RUNTESTDIR/dummyssh"
  > [alias]
  > debugobsolete=debugobsolete -d '0 0'
  > EOF

  $ hg init main

  $ hg -R main debugbuilddag '.+7'

  $ for node in `hg -R main log -T '{node}\n'`; do
  >     printf $node | grep -o . | sort |tr -d "\n" > ancfile
  >     anc=`cat ancfile`
  >     rm ancfile
  >     echo "marking $anc as predecessors of $node"
  >     hg -R main debugobsolete $anc $node
  > done
  marking 000011223334456677789aaaaabbbbcccddddeef as predecessors of 4de32a90b66cd083ebf3c00b41277aa7abca51dd
  1 new obsolescence markers
  marking 012234455555666699aaaaabbbccccccefffffff as predecessors of f69452c5b1af6cbaaa56ef50cf94fff5bcc6ca23
  1 new obsolescence markers
  marking 00001122233445555777778889999abbcccddeef as predecessors of c8d03c1b5e94af74b772900c58259d2e08917735
  1 new obsolescence markers
  marking 0011222445667777889999aabbbbcddddeeeeeee as predecessors of bebd167eb94d257ace0e814aeb98e6972ed2970d
  1 new obsolescence markers
  marking 000011222223344555566778899aaaabccddefff as predecessors of 2dc09a01254db841290af0538aa52f6f52c776e3
  1 new obsolescence markers
  marking 01111222223333444455555566999abbbbcceeef as predecessors of 01241442b3c2bf3211e593b549c655ea65b295e3
  1 new obsolescence markers
  marking 01122444445555566677888aabbcccddddefffff as predecessors of 66f7d451a68b85ed82ff5fcc254daf50c74144bd
  1 new obsolescence markers
  marking 000111111234444467777889999aaaabcdeeeeff as predecessors of 1ea73414a91b0920940797d8fc6a11e447f8ea1e
  1 new obsolescence markers

  $ hg debugobsolete -R main
  000011223334456677789aaaaabbbbcccddddeef 4de32a90b66cd083ebf3c00b41277aa7abca51dd 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}
  012234455555666699aaaaabbbccccccefffffff f69452c5b1af6cbaaa56ef50cf94fff5bcc6ca23 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}
  00001122233445555777778889999abbcccddeef c8d03c1b5e94af74b772900c58259d2e08917735 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}
  0011222445667777889999aabbbbcddddeeeeeee bebd167eb94d257ace0e814aeb98e6972ed2970d 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}
  000011222223344555566778899aaaabccddefff 2dc09a01254db841290af0538aa52f6f52c776e3 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}
  01111222223333444455555566999abbbbcceeef 01241442b3c2bf3211e593b549c655ea65b295e3 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}
  01122444445555566677888aabbcccddddefffff 66f7d451a68b85ed82ff5fcc254daf50c74144bd 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}
  000111111234444467777889999aaaabcdeeeeff 1ea73414a91b0920940797d8fc6a11e447f8ea1e 0 (Thu Jan 01 00:00:00 1970 +0000) {'user': 'test'}

Cache mode is "auto" so local commit did not warm the cache yet

  $ f -s main/.hg/cache/evoext*
  main/.hg/cache/evoext-obscache-00: size=72

Initial push
------------

  $ hg init server
  $ hg -R main push ssh://user@dummy/server
  pushing to ssh://user@dummy/server
  searching for changes
  OBSEXC: computing relevant nodes
  OBSEXC: looking for common markers in 8 nodes
  OBSEXC: computing markers relevant to 8 nodes
  remote: adding changesets
  remote: adding manifests
  remote: adding file changes
  remote: added 8 changesets with 0 changes to 0 files
  remote: 8 new obsolescence markers

sever cash is warm

  $ f -s server/.hg/cache/evoext*
  server/.hg/cache/evoext-depthcache-00: size=88
  server/.hg/cache/evoext-firstmerge-00: size=88
  server/.hg/cache/evoext-obscache-00: size=72
  server/.hg/cache/evoext-stablesortcache-00: size=92
  server/.hg/cache/evoext_obshashrange_v2.sqlite: size=?* (glob)
  server/.hg/cache/evoext_stablerange_v2.sqlite: size=?* (glob)

client cash is warm

  $ f -s main/.hg/cache/evoext*
  main/.hg/cache/evoext-depthcache-00: size=88
  main/.hg/cache/evoext-firstmerge-00: size=88
  main/.hg/cache/evoext-obscache-00: size=72
  main/.hg/cache/evoext-stablesortcache-00: size=92
  main/.hg/cache/evoext_obshashrange_v2.sqlite: size=?* (glob)
  main/.hg/cache/evoext_stablerange_v2.sqlite: size=?* (glob)

initial pull
------------

  $ rm -rf main
  $ hg init main
  $ hg -R main pull ssh://user@dummy/server
  pulling from ssh://user@dummy/server
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 8 changesets with 0 changes to 0 files
  8 new obsolescence markers
  new changesets 1ea73414a91b:4de32a90b66c
  (run 'hg update' to get a working copy)

client cache is empty because the discovery was empty

  $ f -s main/.hg/cache/evoext*
  main/.hg/cache/evoext-obscache-00: size=72

no op pull
------------

clear cache

  $ rm -rf main/.hg/cache/evoext

pull nothing

  $ hg -R main pull ssh://user@dummy/server
  pulling from ssh://user@dummy/server
  searching for changes
  no changes found
  OBSEXC: looking for common markers in 8 nodes

client cash is warm

  $ f -s main/.hg/cache/evoext*
  main/.hg/cache/evoext-depthcache-00: size=88
  main/.hg/cache/evoext-firstmerge-00: size=88
  main/.hg/cache/evoext-obscache-00: size=72
  main/.hg/cache/evoext-stablesortcache-00: size=92
  main/.hg/cache/evoext_obshashrange_v2.sqlite: size=?* (glob)
  main/.hg/cache/evoext_stablerange_v2.sqlite: size=?* (glob)

no op push
------------

clear cache

  $ rm -rf main/.hg/cache/evoext

push nothing

  $ hg -R main push ssh://user@dummy/server
  pushing to ssh://user@dummy/server
  searching for changes
  OBSEXC: computing relevant nodes
  OBSEXC: looking for common markers in 8 nodes
  OBSEXC: markers already in sync
  no changes found
  [1]

client cash is warm

  $ f -s main/.hg/cache/evoext*
  main/.hg/cache/evoext-depthcache-00: size=88
  main/.hg/cache/evoext-firstmerge-00: size=88
  main/.hg/cache/evoext-obscache-00: size=72
  main/.hg/cache/evoext-stablesortcache-00: size=92
  main/.hg/cache/evoext_obshashrange_v2.sqlite: size=?* (glob)
  main/.hg/cache/evoext_stablerange_v2.sqlite: size=?* (glob)
