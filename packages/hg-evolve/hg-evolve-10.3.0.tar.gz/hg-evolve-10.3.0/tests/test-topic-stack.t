  $ . "$TESTDIR/testlib/topic_setup.sh"

Initial setup


  $ cat << EOF >> $HGRCPATH
  > [ui]
  > logtemplate = {rev} {branch} \{{get(namespaces, "topics")}} {phase} {desc|firstline}\n
  > [experimental]
  > evolution=all
  > EOF

  $ hg init main
  $ cd main
  $ hg topic other
  marked working directory as topic: other
  $ echo aaa > aaa
  $ hg add aaa
  $ hg commit -m c_a
  active topic 'other' grew its first changeset
  (see 'hg help topics' for more information)
  $ echo aaa > bbb
  $ hg add bbb
  $ hg commit -m c_b
  $ hg topic foo
  $ echo aaa > ccc
  $ hg add ccc
  $ hg commit -m c_c
  active topic 'foo' grew its first changeset
  (see 'hg help topics' for more information)
  $ echo aaa > ddd
  $ hg add ddd
  $ hg commit -m c_d
  $ echo aaa > eee
  $ hg add eee
  $ hg commit -m c_e
  $ echo aaa > fff
  $ hg add fff
  $ hg commit -m c_f
  $ hg log -G
  @  5 default {foo} draft c_f
  |
  o  4 default {foo} draft c_e
  |
  o  3 default {foo} draft c_d
  |
  o  2 default {foo} draft c_c
  |
  o  1 default {other} draft c_b
  |
  o  0 default {other} draft c_a
  

Check that topic without any parent does not crash --list
---------------------------------------------------------

  $ hg up other
  switching to topic other
  0 files updated, 0 files merged, 4 files removed, 0 files unresolved
  $ hg topic --list
  ### topic: other
  ### target: default (branch)
  s2@ c_b (current)
  s1: c_a
  $ hg phase --public 'topic("other")'
  active topic 'other' is now empty
  (use 'hg topic --clear' to clear it if needed)

After changing the phase of all the changesets in "other" to public, the topic should still be active, but is empty. We should be better at informing the user about it and displaying good data in this case.

  $ hg topic
     foo   (4 changesets)
   * other (0 changesets)
  $ hg stack
  ### topic: other
  ### target: default (branch)
  (stack is empty)
  s0^ c_b (base current)

  $ hg up foo
  switching to topic foo
  4 files updated, 0 files merged, 0 files removed, 0 files unresolved

Simple test
-----------

'hg stack' list all changeset in the topic

  $ hg topic
   * foo (4 changesets)
  $ hg stack
  ### topic: foo
  ### target: default (branch)
  s4@ c_f (current)
  s3: c_e
  s2: c_d
  s1: c_c
  s0^ c_b (base)
  $ hg stack -v
  ### topic: foo
  ### target: default (branch)
  s4(6559e6d93aea)@ c_f (current)
  s3(0f9ac936c87d): c_e
  s2(e629654d7050): c_d
  s1(8522f9e3fee9): c_c
  s0(ea705abc4f51)^ c_b (base)
  $ hg stack -Tjson | "$PYTHON" -m json.tool
  [
      {
          "desc": "c_f",
          "isentry": true,
          "node": "6559e6d93aeadba940874f54f106c61931b5b8cf",
          "stack_index": 4,
          "state": [
              "current"
          ],
          "symbol": "@"
      },
      {
          "desc": "c_e",
          "isentry": true,
          "node": "0f9ac936c87d1d991011862aff4e86d0c3300a89",
          "stack_index": 3,
          "state": [
              "clean"
          ],
          "symbol": ":"
      },
      {
          "desc": "c_d",
          "isentry": true,
          "node": "e629654d70505107cca3d12782d9c5a50d8fb9c8",
          "stack_index": 2,
          "state": [
              "clean"
          ],
          "symbol": ":"
      },
      {
          "desc": "c_c",
          "isentry": true,
          "node": "8522f9e3fee92d4ec4e688ac3fbd2ee0f8fd5036",
          "stack_index": 1,
          "state": [
              "clean"
          ],
          "symbol": ":"
      },
      {
          "desc": "c_b",
          "isentry": false,
          "node": "ea705abc4f51e26d356ed94b3443e8c19b76cedf",
          "stack_index": 0,
          "state": [
              "base"
          ],
          "symbol": "^"
      }
  ]
  $ hg stack -v -Tjson | "$PYTHON" -m json.tool
  [
      {
          "desc": "c_f",
          "isentry": true,
          "node": "6559e6d93aeadba940874f54f106c61931b5b8cf",
          "stack_index": 4,
          "state": [
              "current"
          ],
          "symbol": "@"
      },
      {
          "desc": "c_e",
          "isentry": true,
          "node": "0f9ac936c87d1d991011862aff4e86d0c3300a89",
          "stack_index": 3,
          "state": [
              "clean"
          ],
          "symbol": ":"
      },
      {
          "desc": "c_d",
          "isentry": true,
          "node": "e629654d70505107cca3d12782d9c5a50d8fb9c8",
          "stack_index": 2,
          "state": [
              "clean"
          ],
          "symbol": ":"
      },
      {
          "desc": "c_c",
          "isentry": true,
          "node": "8522f9e3fee92d4ec4e688ac3fbd2ee0f8fd5036",
          "stack_index": 1,
          "state": [
              "clean"
          ],
          "symbol": ":"
      },
      {
          "desc": "c_b",
          "isentry": false,
          "node": "ea705abc4f51e26d356ed94b3443e8c19b76cedf",
          "stack_index": 0,
          "state": [
              "base"
          ],
          "symbol": "^"
      }
  ]

  $ hg stack -T '{rev}: [{branch}] [{topic}] {desc}\n'
  5: [default] [foo] c_f
  4: [default] [foo] c_e
  3: [default] [foo] c_d
  2: [default] [foo] c_c
  1: [default] [] c_b

check that topics and stack are available even if ui.strict=true

  $ hg topics
   * foo (4 changesets)
  $ hg stack
  ### topic: foo
  ### target: default (branch)
  s4@ c_f (current)
  s3: c_e
  s2: c_d
  s1: c_c
  s0^ c_b (base)
  $ hg topics --config ui.strict=true
   * foo (4 changesets)
  $ hg stack --config ui.strict=true
  ### topic: foo
  ### target: default (branch)
  s4@ c_f (current)
  s3: c_e
  s2: c_d
  s1: c_c
  s0^ c_b (base)

merge case (displaying info about external)
-------------------------------------------

  $ hg up default
  0 files updated, 0 files merged, 4 files removed, 0 files unresolved
  $ hg topics zzz
  marked working directory as topic: zzz
  $ echo zzz > zzz
  $ hg add zzz
  $ hg commit -m zzz_a
  active topic 'zzz' grew its first changeset
  (see 'hg help topics' for more information)
  $ hg merge foo
  4 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg commit -m "merged foo"

stack -m display data about child

  $ hg stack foo
  ### topic: foo
  ### target: default (branch)
  s4: c_f
  s3: c_e
  s2: c_d
  s1: c_c
  s0^ c_b (base)

  $ hg stack foo --children
  ### topic: foo
  ### target: default (branch)
  s4: c_f (external-children)
  s3: c_e
  s2: c_d
  s1: c_c
  s0^ c_b (base)

error case, nothing to list

  $ hg strip --config extensions.strip= t1 --no-backup
  0 files updated, 0 files merged, 5 files removed, 0 files unresolved

  $ hg up foo
  switching to topic foo
  4 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg topic --clear
  $ hg stack
  ### target: default (branch)
  (stack is empty)
  s0^ c_f (base current)

Test "t#" reference
-------------------


  $ hg up s2
  abort: cannot resolve "s2": branch "default" has only 0 non-public changesets
  [255]
  $ hg topic foo
  marked working directory as topic: foo
  $ hg up t42
  abort: cannot resolve "t42": topic "foo" has only 4 changesets
  [255]
  $ hg up s42
  abort: cannot resolve "s42": topic "foo" has only 4 changesets
  [255]
  $ hg up s2
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ hg summary
  parent: 3:e629654d7050 
   c_d
  branch: default:foo
  commit: (clean)
  update: 2 new changesets (update)
  phases: 4 draft
  topic:  foo

Case with some of the topic unstable
------------------------------------

  $ echo bbb > ddd
  $ hg commit --amend
  2 new orphan changesets
  $ hg log -G
  @  6 default {foo} draft c_d
  |
  | *  5 default {foo} draft c_f
  | |
  | *  4 default {foo} draft c_e
  | |
  | x  3 default {foo} draft c_d
  |/
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  
  $ hg topic --list
  ### topic: foo
  ### target: default (branch)
  s4$ c_f (orphan)
  s3$ c_e (orphan)
  s2@ c_d (current)
  s1: c_c
  s0^ c_b (base)
  $ hg up s3
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg topic --list
  ### topic: foo
  ### target: default (branch)
  s4$ c_f (orphan)
  s3@ c_e (current orphan)
  s2: c_d
  s1: c_c
  s0^ c_b (base)
  $ hg topic --list --color=debug
  [stack.summary.topic|### topic: [topic.active|foo]]
  [stack.summary.branches|### target: default (branch)]
  [stack.index stack.index.orphan|s4][stack.state stack.state.orphan|$] [stack.desc stack.desc.orphan|c_f][stack.state stack.state.orphan| (orphan)]
  [stack.index stack.index.current stack.index.orphan|s3][stack.state stack.state.current stack.state.orphan|@] [stack.desc stack.desc.current stack.desc.orphan|c_e][stack.state stack.state.current stack.state.orphan| (current orphan)]
  [stack.index stack.index.clean|s2][stack.state stack.state.clean|:] [stack.desc stack.desc.clean|c_d]
  [stack.index stack.index.clean|s1][stack.state stack.state.clean|:] [stack.desc stack.desc.clean|c_c]
  [stack.index stack.index.base|s0][stack.state stack.state.base|^] [stack.desc stack.desc.base|c_b][stack.state stack.state.base| (base)]
  $ hg up s2
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved

Also test the revset:

  $ hg log -r 'stack()'
  2 default {foo} draft c_c
  6 default {foo} draft c_d
  4 default {foo} draft c_e
  5 default {foo} draft c_f

  $ hg log -r 'stack(foo)'
  hg: parse error: stack takes no arguments, it works on current topic
  [10]

  $ hg log -r 'stack(foobar)'
  hg: parse error: stack takes no arguments, it works on current topic
  [10]

Stack relation:

  $ hg log -r 'foo#stack'
  2 default {foo} draft c_c
  4 default {foo} draft c_e
  5 default {foo} draft c_f
  6 default {foo} draft c_d

Stack relation subscript:

  $ hg log -r 'foo#stack[0]'
  1 default {} public c_b
  $ hg log -r 's0 and foo#stack[0]'
  1 default {} public c_b
  $ hg log -r 'foo#stack[4]'
  5 default {foo} draft c_f
  $ hg log -r 's4 and foo#stack[4]'
  5 default {foo} draft c_f

Case with multiple heads on the topic
-------------------------------------

Make things linear again

  $ hg rebase -s 'desc(c_e)' -d 'desc(c_d) - obsolete()'
  rebasing 4:0f9ac936c87d foo "c_e"
  rebasing 5:6559e6d93aea foo "c_f"
  $ hg log -G
  o  8 default {foo} draft c_f
  |
  o  7 default {foo} draft c_e
  |
  @  6 default {foo} draft c_d
  |
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  


Create the second branch

  $ hg up 'desc(c_d)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo aaa > ggg
  $ hg add ggg
  $ hg commit -m c_g
  $ echo aaa > hhh
  $ hg add hhh
  $ hg commit -m c_h
  $ hg log -G
  @  10 default {foo} draft c_h
  |
  o  9 default {foo} draft c_g
  |
  | o  8 default {foo} draft c_f
  | |
  | o  7 default {foo} draft c_e
  |/
  o  6 default {foo} draft c_d
  |
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  

Test output

  $ hg top -l
  ### topic: foo (2 heads)
  ### target: default (branch)
  s6@ c_h (current)
  s5: c_g
  s2^ c_d (base)
  s4: c_f
  s3: c_e
  s2: c_d
  s1: c_c
  s0^ c_b (base)

Case with multiple heads on the topic with instability involved
---------------------------------------------------------------

We amend the message to make sure the display base picks the right changeset

  $ hg up 'desc(c_d)'
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo ccc > ddd
  $ hg commit --amend -m 'c_D' 
  4 new orphan changesets
  $ hg rebase -d . -s 'desc(c_g)'
  rebasing 9:81264ae8a36a foo "c_g"
  rebasing 10:fde5f5941642 foo "c_h"
  $ hg log -G
  o  13 default {foo} draft c_h
  |
  o  12 default {foo} draft c_g
  |
  @  11 default {foo} draft c_D
  |
  | *  8 default {foo} draft c_f
  | |
  | *  7 default {foo} draft c_e
  | |
  | x  6 default {foo} draft c_d
  |/
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  

  $ hg topic --list
  ### topic: foo (2 heads)
  ### target: default (branch)
  s6: c_h
  s5: c_g
  s2^ c_D (base current)
  s4$ c_f (orphan)
  s3$ c_e (orphan)
  s2@ c_D (current)
  s1: c_c
  s0^ c_b (base)

Trying to list non existing topic
  $ hg stack thisdoesnotexist
  abort: cannot resolve "thisdoesnotexist": no such topic found
  [255]
  $ hg topic --list thisdoesnotexist
  abort: cannot resolve "thisdoesnotexist": no such topic found
  [255]

Complex cases where commits with same topic are not consecutive but are linear
==============================================================================

  $ hg log --graph
  o  13 default {foo} draft c_h
  |
  o  12 default {foo} draft c_g
  |
  @  11 default {foo} draft c_D
  |
  | *  8 default {foo} draft c_f
  | |
  | *  7 default {foo} draft c_e
  | |
  | x  6 default {foo} draft c_d
  |/
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  
Converting into a linear chain
  $ hg rebase -s 'desc("c_e") - obsolete()' -d 'desc("c_h") - obsolete()'
  rebasing 7:215bc359096a foo "c_e"
  rebasing 8:ec9267b3f33f foo "c_f"

  $ hg log -G
  o  15 default {foo} draft c_f
  |
  o  14 default {foo} draft c_e
  |
  o  13 default {foo} draft c_h
  |
  o  12 default {foo} draft c_g
  |
  @  11 default {foo} draft c_D
  |
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  
Changing topics on some commits in between
  $ hg topic foobar -r 'desc(c_e) + desc(c_D)'
  switching to topic foobar
  4 new orphan changesets
  changed topic on 2 changesets to "foobar"
  $ hg log -G
  @  17 default {foobar} draft c_D
  |
  | *  16 default {foobar} draft c_e
  | |
  | | *  15 default {foo} draft c_f
  | | |
  | | x  14 default {foo} draft c_e
  | |/
  | *  13 default {foo} draft c_h
  | |
  | *  12 default {foo} draft c_g
  | |
  | x  11 default {foo} draft c_D
  |/
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  
  $ hg rebase -s 'desc("c_f") - obsolete()' -d 'desc("c_e") - obsolete()'
  rebasing 15:77082e55de88 foo "c_f"
  switching to topic foo
  1 new orphan changesets
  switching to topic foobar
  $ hg rebase -s 'desc("c_g") - obsolete()' -d 'desc("c_D") - obsolete()'
  rebasing 12:0c3e8aed985d foo "c_g"
  switching to topic foo
  rebasing 13:b9e4f3709bc5 foo "c_h"
  rebasing 16:4bc813530301 foobar "c_e"
  switching to topic foobar
  rebasing 18:4406ea4be852 tip foo "c_f"
  switching to topic foo
  switching to topic foobar
  $ hg up
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg log --graph
  o  22 default {foo} draft c_f
  |
  @  21 default {foobar} draft c_e
  |
  o  20 default {foo} draft c_h
  |
  o  19 default {foo} draft c_g
  |
  o  17 default {foobar} draft c_D
  |
  o  2 default {foo} draft c_c
  |
  o  1 default {} public c_b
  |
  o  0 default {} public c_a
  
XXX: The following should show single heads
XXX: The behind count is weird, because the topic are interleaved.

  $ hg stack
  ### topic: foobar
  ### target: default (branch), 3 behind
  s2@ c_e (current)
    ^ c_h
  s1: c_D
  s0^ c_c (base)

  $ hg stack -v
  ### topic: foobar
  ### target: default (branch), 3 behind
  s2(ea0f882ce093)@ c_e (current)
                  ^ c_h
  s1(d2f548af67ab): c_D
  s0(8522f9e3fee9)^ c_c (base)

  $ hg stack --debug
  ### topic: foobar
  ### target: default (branch), 3 behind
  s2(ea0f882ce093a2ad63db49083c5cb98a24a9470e)@ c_e (current)
                                              ^ c_h
  s1(d2f548af67ab55b08452a3e00a539319490fcd5b): c_D
  s0(8522f9e3fee92d4ec4e688ac3fbd2ee0f8fd5036)^ c_c (base)

  $ hg stack foo
  ### topic: foo
  ### target: default (branch), ambiguous rebase destination - topic 'foo' has 3 heads
  s4: c_f
    ^ c_e
  s3: c_h
  s2: c_g
    ^ c_D
  s1: c_c
  s0^ c_b (base)

case involving a merge
----------------------

  $ cd ..
  $ hg init stack-gap-merge
  $ cd stack-gap-merge

  $ echo aaa > aaa
  $ hg commit -Am 'c_A'
  adding aaa
  $ hg topic red
  marked working directory as topic: red
  $ echo bbb > bbb
  $ hg commit -Am 'c_B'
  adding bbb
  active topic 'red' grew its first changeset
  (see 'hg help topics' for more information)
  $ echo ccc > ccc
  $ hg commit -Am 'c_C'
  adding ccc
  $ hg topic blue
  $ echo ddd > ddd
  $ hg commit -Am 'c_D'
  adding ddd
  active topic 'blue' grew its first changeset
  (see 'hg help topics' for more information)
  $ hg up 'desc("c_B")'
  switching to topic red
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo eee > eee
  $ hg commit -Am 'c_E'
  adding eee
  $ echo fff > fff
  $ hg commit -Am 'c_F'
  adding fff
  $ hg topic blue
  $ echo ggg > ggg
  $ hg commit -Am 'c_G'
  adding ggg
  $ hg up 'desc("c_D")'
  2 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ hg topic red
  $ hg merge 'desc("c_G")'
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg commit -Am 'c_H'
  $ hg topic blue
  $ echo iii > iii
  $ hg ci -Am 'c_I'
  adding iii

  $ hg log -G
  @  8 default {blue} draft c_I
  |
  o    7 default {red} draft c_H
  |\
  | o  6 default {blue} draft c_G
  | |
  | o  5 default {red} draft c_F
  | |
  | o  4 default {red} draft c_E
  | |
  o |  3 default {blue} draft c_D
  | |
  o |  2 default {red} draft c_C
  |/
  o  1 default {red} draft c_B
  |
  o  0 default {} draft c_A
  

  $ hg stack red
  ### topic: red
  ### target: default (branch), 6 behind
  s5: c_H
    ^ c_G
    ^ c_D
  s4: c_C
  s1^ c_B (base)
  s3: c_F
  s2: c_E
  s1: c_B
  s0^ c_A (base)
  $ hg stack blue
  ### topic: blue
  ### target: default (branch), ambiguous rebase destination - topic 'blue' has 3 heads
  s3@ c_I (current)
    ^ c_H
  s2: c_D
    ^ c_C
  s1: c_G
  s0^ c_F (base)

Even with some obsolete and orphan changesets

(the ordering of each branch of "blue" change because their hash change. we
should stabilize this eventually)

  $ hg up 'desc("c_B")'
  switching to topic red
  0 files updated, 0 files merged, 6 files removed, 0 files unresolved
  $ hg commit --amend --user test2
  7 new orphan changesets
  $ hg up 'desc("c_C")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg commit --amend --user test2
  $ hg up 'desc("c_D")'
  switching to topic blue
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg commit --amend --user test2

  $ hg log -G --rev 'sort(all(), "topo")'
  @  11 default {blue} draft c_D
  |
  | *  8 default {blue} draft c_I
  | |
  | *    7 default {red} draft c_H
  | |\
  | | *  6 default {blue} draft c_G
  | | |
  | | *  5 default {red} draft c_F
  | | |
  | | *  4 default {red} draft c_E
  | | |
  | x |  3 default {blue} draft c_D
  |/ /
  x /  2 default {red} draft c_C
  |/
  | *  10 default {red} draft c_C
  |/
  x  1 default {red} draft c_B
  |
  | o  9 default {red} draft c_B
  |/
  o  0 default {} draft c_A
  

  $ hg stack red
  ### topic: red
  ### target: default (branch), 7 behind
  s5$ c_H (orphan)
    ^ c_G
    ^ c_D
  s4$ c_C (orphan)
  s1^ c_B (base)
  s3$ c_F (orphan)
  s2$ c_E (orphan)
  s1: c_B
  s0^ c_A (base)
  $ hg stack blue
  ### topic: blue
  ### target: default (branch), ambiguous rebase destination - topic 'blue' has 3 heads
  s3$ c_I (orphan)
    ^ c_H
  s2$ c_G (orphan)
    ^ c_F
  s1@ c_D (current orphan)
  s0^ c_C (base orphan)

more obsolescence

  $ hg up 'max(desc("c_H"))'
  switching to topic red
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg commit --amend --user test3
  $ hg up 'max(desc("c_G"))'
  switching to topic blue
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ hg commit --amend --user test3
  $ hg up 'max(desc("c_B"))'
  switching to topic red
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ hg commit --amend --user test3
  $ hg up 'max(desc("c_C"))'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg commit --amend --user test3
  $ hg up 'max(desc("c_D"))'
  switching to topic blue
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg commit --amend --user test3

  $ hg log -G --rev 'sort(all(), "topo")'
  @  16 default {blue} draft c_D
  |
  | *  13 default {blue} draft c_G
  | |
  | | *    12 default {red} draft c_H
  | | |\
  | | | | *  8 default {blue} draft c_I
  | | | | |
  | | +---x  7 default {red} draft c_H
  | | | |/
  | +---x  6 default {blue} draft c_G
  | | |
  | * |  5 default {red} draft c_F
  | | |
  | * |  4 default {red} draft c_E
  | | |
  +---x  3 default {blue} draft c_D
  | |
  x |  2 default {red} draft c_C
  |/
  | *  15 default {red} draft c_C
  |/
  x  1 default {red} draft c_B
  |
  | o  14 default {red} draft c_B
  |/
  o  0 default {} draft c_A
  

  $ hg stack red
  ### topic: red
  ### target: default (branch), 7 behind
  s5$ c_H (orphan)
    ^ c_G
    ^ c_D
  s4$ c_F (orphan)
  s3$ c_E (orphan)
  s1^ c_B (base)
  s2$ c_C (orphan)
  s1: c_B
  s0^ c_A (base)
  $ hg stack blue
  ### topic: blue
  ### target: default (branch), ambiguous rebase destination - topic 'blue' has 3 heads
  s3$ c_I (orphan)
    ^ c_H
  s2$ c_G (orphan)
    ^ c_F
  s1@ c_D (current orphan)
  s0^ c_C (base orphan)

Test stack behavior with a split
--------------------------------

get things linear again

  $ hg rebase -r s1 -d default
  rebasing 16:1d84ec948370 tip blue "c_D"
  switching to topic blue
  $ hg rebase -r s2 -d s1
  rebasing 13:3ab2eedae500 blue "c_G"
  $ hg rebase -r s3 -d s2
  rebasing 8:3bfe800e0486 blue "c_I"
  $ hg stack
  ### topic: blue
  ### target: default (branch)
  s3: c_I
  s2: c_G
  s1@ c_D (current)
  s0^ c_A (base)

making a split
(first get something to split)

  $ hg up s2
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg status --change .
  A ggg
  $ echo zzz > Z
  $ hg add Z
  $ hg commit --amend
  1 new orphan changesets
  $ hg status --change .
  A Z
  A ggg
  $ hg stack
  ### topic: blue
  ### target: default (branch)
  s3$ c_I (orphan)
  s2@ c_G (current)
  s1: c_D
  s0^ c_A (base)
  $ hg --config extensions.evolve=  --config ui.interactive=yes split << EOF
  > y
  > y
  > n
  > c
  > EOF
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  adding Z
  adding ggg
  diff --git a/Z b/Z
  new file mode 100644
  examine changes to 'Z'?
  (enter ? for help) [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +zzz
  record change 1/2 to 'Z'?
  (enter ? for help) [Ynesfdaq?] y
  
  diff --git a/ggg b/ggg
  new file mode 100644
  examine changes to 'ggg'?
  (enter ? for help) [Ynesfdaq?] n
  
  continue splitting? [Ycdq?] c

  $ hg debugobsolete
  34679cfcccdd07565970b959c79428af9a5744e4 6a11ae6b0cde4d4952ed68e8077b9e3596d99548 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  20f7945d89a5e372b7548f766ebc800677856443 3c7bec987cd37ba12b83c01683e8609dd549c07b 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  952e24687ebc5f11743268f6f1c3f24fa83c7ddd 74979543bf1d6c0f75229991400f352a6fb3fddb 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  c9961f97c7b40b54b3c1922986675d6f38793014 d7bfa3d6ce36dfb917547246752f0c2a564fe33b 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  c7d60a180d05255e8c6ea50bce09d014015b7cdc 3ab2eedae500f52b6aa220bb8ce6e20732a8a6d1 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  6a11ae6b0cde4d4952ed68e8077b9e3596d99548 61700bf67137c724a72aa5f034e9187d2c5e7e47 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  3c7bec987cd37ba12b83c01683e8609dd549c07b 4bcfa5dd0945476ba938e8115e81ba367af3b573 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  74979543bf1d6c0f75229991400f352a6fb3fddb 1d84ec948370a2ac1a51f3ab27835e31d50c3407 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '16', 'operation': 'amend', 'user': 'test'}
  1d84ec948370a2ac1a51f3ab27835e31d50c3407 f3328cd199dc389b850ca952f65a15a8e6dbc79b 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  3ab2eedae500f52b6aa220bb8ce6e20732a8a6d1 907f7d3c2333082d62942ac3a47e466ce03d82b9 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  3bfe800e04863d23f909f8d98848656b7b5a971a 662ff4ad29901b325a64c39f7850e3efaaeeccc5 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '4', 'operation': 'rebase', 'user': 'test'}
  907f7d3c2333082d62942ac3a47e466ce03d82b9 b24bab30ac12f6124a52e74aaf46b7468e42526c 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '8', 'operation': 'amend', 'user': 'test'}
  b24bab30ac12f6124a52e74aaf46b7468e42526c dde94df880e97f4a1ee8c5408254b429b3d90204 e7ea874afbd5c17aeee366d39a828dbcb01682ce 0 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '12', 'operation': 'split', 'user': 'test'}
  $ hg --config extensions.evolve= obslog --all
  o  dde94df880e9 (21) c_G
  |    split(parent, content) from b24bab30ac12 using split by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  | @  e7ea874afbd5 (22) c_G
  |/     split(parent, content) from b24bab30ac12 using split by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  b24bab30ac12 (20) c_G
  |    amended(content) from 907f7d3c2333 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  907f7d3c2333 (18) c_G
  |    rebased(parent) from 3ab2eedae500 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  3ab2eedae500 (13) c_G
  |    reauthored(user) from c7d60a180d05 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  c7d60a180d05 (6) c_G
  
  $ hg export .
  # HG changeset patch
  # User test3
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID e7ea874afbd5c17aeee366d39a828dbcb01682ce
  # Parent  dde94df880e97f4a1ee8c5408254b429b3d90204
  # EXP-Topic blue
  c_G
  
  diff -r dde94df880e9 -r e7ea874afbd5 ggg
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/ggg	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +ggg
  $ hg export .^
  # HG changeset patch
  # User test3
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID dde94df880e97f4a1ee8c5408254b429b3d90204
  # Parent  f3328cd199dc389b850ca952f65a15a8e6dbc79b
  # EXP-Topic blue
  c_G
  
  diff -r f3328cd199dc -r dde94df880e9 Z
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/Z	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +zzz

Check that stack output still makes sense

  $ hg stack
  ### topic: blue
  ### target: default (branch)
  s4$ c_I (orphan)
  s3@ c_G (current)
  s2: c_G
  s1: c_D
  s0^ c_A (base)
