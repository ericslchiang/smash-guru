"""
Author: ericslchiang
Description: Pulls tournament brackets from smash.gg, and return the number of 
players in the simulation bracket. 
"""
from __future__ import print_function
import pysmash
import pprint



smash = pysmash.SmashGG()
def init_sim_bracket():
    pp = pprint.PrettyPrinter(indent=4)
    brackets = smash.tournament_show_event_brackets("get-on-my-level-2016",
    												"melee-singles")
    bracket_players = smash.bracket_show_players(brackets['bracket_ids'[-1]])
    return len(bracket_players)


if __name__ == "__main__":
    print(init_sim_bracket())
