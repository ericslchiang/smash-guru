"""
Author: ericslchiang
Description: Pulls tournament brackets from smash.gg, and return the number of 
players in the simulation bracket, which is then used return the top seeds of 
the bracket.
"""
from __future__ import print_function
import pysmash
import pprint



smash = pysmash.SmashGG()
pp = pprint.PrettyPrinter(indent=4)
def init_sim_bracket(tournament_name, tournament_event):
    brackets = smash.tournament_show_event_brackets(tournament_name,
                                                    tournament_event)
    bracket_players = smash.bracket_show_players(brackets['bracket_ids'][-1])
    return len(bracket_players)

def get_top_player(tournament_name, tournament_event): 
    players = smash.tournament_show_players(tournament_name, tournament_event)
    players.sort(key=lambda player: player["seed"])
    bracket_size = init_sim_bracket(tournament_name, tournament_event)
    return players[:bracket_size]

if __name__ == "__main__":
    tournament_name = "get-on-my-level-2016"
    tournament_event ="melee-singles"
    print(init_sim_bracket(tournament_name, tournament_event))
    pp.pprint(get_top_player(tournament_name, tournament_event))
