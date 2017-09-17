import pysmash
import pprint

# init the wrapper class
smash = pysmash.SmashGG()
pp = pprint.PrettyPrinter(indent=4)

# All results are represented as normal Python dicts
# Bracket Method usage

# show players given a bracket_id
brackets = smash.tournament_show_event_brackets('hidden-bosses-4-0', 'wii-u-singles')
bracket_players = smash.bracket_show_players(brackets['bracket_ids'][0])  # <- bracket_id
players = smash.tournament_show_players('hidden-bosses-4-0', 'wii-u-singles')
pp.pprint(players)


# bracket_players = smash.bracket_show_players(224997) # <- if you know the id before hand
# pp.pprint(bracket_players)

# show played sets for a bracket
# This method ignores sets without a recorded score (Smash.gg "oddity". Either the set was not played or the set
# potentially fed into another bracket.)
brackets = smash.tournament_show_event_brackets('hidden-bosses-4-0', 'wii-u-singles')
sets =  smash.bracket_show_sets(brackets['bracket_ids'][0]) # <- bracket_id
# sets = self.smash.bracket_show_sets(225024) # <- if you know the id before hand

# pp.pprint(sets)

player_head_to_head = smash.tournament_show_head_to_head('get-on-my-level-2016', 'hungrybox', 'armada', 'melee-singles')
pp.pprint(player_head_to_head)

