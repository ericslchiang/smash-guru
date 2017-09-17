from __future__ import print_function


def print_tree(rootnode):
  thislevel = [rootnode]
  while thislevel:
    nextlevel = list()
    for n in thislevel:
        # TODO(ericslchiang): Change "{"tag": ""}" to None
        print("{} v.s. {}".format(n.player_one["tag"], n.player_two["tag"]),
              end=" | ")
        if n.left:
            nextlevel.append(n.left)
        if n.right:
            nextlevel.append(n.right)
    print("\n")
    thislevel = nextlevel

