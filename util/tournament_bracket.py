"""
Author: austinscchiang
Description: Given raw parsed data, parse the file for a placing-to-fantasy-
points key-value pair. Collect all key-value pairs and stream the complete
placing-to-points conversion into an output file.
"""
from __future__ import print_function
import pysmash
import pprint



smash = pysmash.SmashGG()
def init_sim_bracket():
    pp = pprint.PrettyPrinter(indent=4)
    brackets = smash.tournament_show_event_brackets("get-on-my-level-2016", "melee-singles")
    #pp.pprint(brackets)
    bracket_players = smash.bracket_show_players(brackets['bracket_ids'[-1]])  # <- bracket_id
    # bracket_players = smash.bracket_show_players(224997) # <- if you know the id before hand
    #pp.pprint(bracket_players)
    return len(bracket_players)


if __name__ == "__main__":
    print(init_sim_bracket())
