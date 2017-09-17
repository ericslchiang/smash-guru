"""
Author: ericslchiang
Description: Pulls tournament brackets from smash.gg, and return the number of 
players in the simulation bracket, which is then used return the top seeds of 
the bracket.
"""
#TODO(ericslchiang): Change "{"tag": ""}" to None
from __future__ import print_function
import pysmash
import pprint
from math import log

class TreeNode(object):
    def __init__(self):
        self.player_one = {"tag": ""}
        self.player_two = {"tag": ""}

        self.left = None
        self.right = None

def knapSack(budget, cost, val):
    n = len(val)
    K = [[0 for x in range(budget+1)] for x in range(n+1)]
 
    # Build table K[][] in bottom up manner
    for i in range(n+1):
        for w in range(budget+1):
            if i==0 or w==0:
                K[i][w] = 0
            elif cost[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-cost[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
 
    return K[n][budget]
 
def traverse(rootnode):
  thislevel = [rootnode]
  while thislevel:
    nextlevel = list()
    for n in thislevel:
        print("{} v.s. {}".format(n.player_one["tag"], n.player_two["tag"]), end="")
        if n.left:
            nextlevel.append(n.left)
        if n.right:
            nextlevel.append(n.right)
    print("\n")
    thislevel = nextlevel


smash = pysmash.SmashGG()
pp = pprint.PrettyPrinter(indent=4)
def init_sim_bracket(tournament_name, tournament_event):
    brackets = smash.tournament_show_event_brackets(tournament_name,
                                                    tournament_event)
    bracket_players = smash.bracket_show_players(brackets['bracket_ids'][-1])
    return len(bracket_players)

def get_top_players(tournament_name, tournament_event): 
    players = smash.tournament_show_players(tournament_name, tournament_event)
    players.sort(key=lambda player: player["seed"])
    bracket_size = init_sim_bracket(tournament_name, tournament_event)
    return players[:bracket_size]

def build_bracket_tree(bracket_depth, players):
    new_node = TreeNode()
    if bracket_depth == 1:
        new_node.player_one = players.pop()
        new_node.player_two = players.pop()
    #Fix seeding later, for now fill in order

    else:
        new_node.left = build_bracket_tree(bracket_depth-1, players)
        new_node.right = build_bracket_tree(bracket_depth-1, players)
        
    return new_node

if __name__ == "__main__":
    tournament_name = "get-on-my-level-2016"
    tournament_event ="melee-singles"
    top_players = get_top_players(tournament_name, tournament_event)
    num_top_players = len(top_players)
    bracket_size = init_sim_bracket(tournament_name, tournament_event)
    print(bracket_size)
    winners_players = top_players[:num_top_players/2]
    winners_players.reverse()
    losers_players = top_players[num_top_players/2:]
    losers_players.reverse()
    winners_bracket = build_bracket_tree(log(bracket_size/2, 2), winners_players)
    losers_bracket = build_bracket_tree(log(bracket_size/2, 2), losers_players)

    traverse(winners_bracket)
    traverse(losers_bracket)
    """
    Test cases for the optimization program
    val = [60, 100, 120]
    cost = [10, 20, 30]
    budget = 50

    print(knapSack(budget, cost, val))
    """
    