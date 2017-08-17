"""
Author: austinscchiang
Description: Given raw parsed data, parse the file for a placing-to-fantasy-
points key-value pair. Collect all key-value pairs and stream the complete
placing-to-points conversion into an output file.
"""
from __future__ import print_function
import pysmash

smash = pysmash.SmashGG()
def test():
    tournament = smash.tournament_show_with_brackets("get-on-my-level-2016",
                                                     "melee-singles")
    print(tournament)

if __name__ == "__main__":
    test()
