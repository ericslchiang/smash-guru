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
from math import log, exp
from head_to_head import head_to_head_read


class TreeNode(object):
    def __init__(self):
        self.player_one = {"tag": ""}
        self.player_two = {"tag": ""}

        self.left = None
        self.right = None

def knapSack(budget, cost, val):
    n = len(val)
    dp= [[0 for x in range(budget+1)] for x in range(n+1)]
 
    # Build table K[][] in bottom up manner
    for i in range(n+1):
        for w in range(budget+1):
            if i==0 or w==0:
                dp[i][w] = 0
            elif cost[i-1] <= w:
                dp[i][w] = max(val[i-1] + dp[i-1][w-cost[i-1]],  dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
 
    return dp[n][budget]
 
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

#For now program assumes the user inputs the higher seed first and the 
#lower seed second. A fix will be implemented at a later time.
def winrate(player_1, player_2, tag_rank, head_to_head):
    if (player_1["seed"] > player_2["seed"]):
        lo_seed = player_1["seed"]
        hi_seed = player_2["seed"]
        lo_seed_tag = player_1["tag"].lower()
        hi_seed_tag = player_2["tag"].lower()
    else:
        hi_seed = player_1["seed"]
        lo_seed = player_2["seed"]
        hi_seed_tag = player_1["tag"].lower()
        lo_seed_tag = player_2["tag"].lower()

    
    hi_seed_index = None
    lo_seed_index = None
    if hi_seed_tag in tag_rank:
        hi_seed_index = tag_rank[hi_seed_tag]
    if lo_seed_tag in tag_rank:
        lo_seed_index = tag_rank[lo_seed_tag]
    if not lo_seed_index:
        return 1.0
    if not hi_seed_index:
        return 0.0
    hi_seed_set_win_lo_seed = head_to_head[hi_seed_index][lo_seed_index]
    lo_seed_set_win_hi_seed = head_to_head[lo_seed_index][hi_seed_index]
    hi_seed_winrate = (0.5 / (1 + exp(-(lo_seed - hi_seed))) + 
                 0.5 * (hi_seed_set_win_lo_seed/(hi_seed_set_win_lo_seed + lo_seed_set_win_hi_seed)))
    return hi_seed_winrate

def bracket_builder(tournament_name, tournament_event, top_players):
    num_top_players = len(top_players)
    bracket_size = init_sim_bracket(tournament_name, tournament_event)
    winners_players = top_players[:num_top_players/2]
    winners_players.reverse()
    losers_players = top_players[num_top_players/2:]
    losers_players.reverse()
    winners_bracket = build_bracket_tree(log(bracket_size/2, 2), winners_players)
    losers_bracket = build_bracket_tree(log(bracket_size/2, 2), losers_players)
    return (winners_bracket, losers_bracket)

if __name__ == "__main__":    
    top_players = get_top_players("get-on-my-level-2016", "melee-singles")
    winners_bracket, losers_bracket = bracket_builder("get-on-my-level-2016", "melee-singles", top_players)
    traverse(winners_bracket)
    traverse(losers_bracket)

    tag_rank, head_to_head = head_to_head_read("head_to_head.txt")
    print(winrate(top_players[2], top_players[3], tag_rank, head_to_head))
