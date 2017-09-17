"""
Author: ericslchiang
Description: Pulls tournament brackets from smash.gg, and return the number of 
players in the simulation bracket, which is then used return the top seeds of 
the bracket.
"""

from __future__ import print_function
import pysmash
import pprint
from math import log
from head_to_head import head_to_head_read
from print_tree import print_tree
from tree_node import TreeNode
from winrate import winrate


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
    # TODO(ericslchiang): Fix seeding later, for now fill in order

    else:
        new_node.left = build_bracket_tree(bracket_depth-1, players)
        new_node.right = build_bracket_tree(bracket_depth-1, players)
        
    return new_node

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
    
    print_tree(winners_bracket)
    print_tree(losers_bracket)

