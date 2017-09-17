from math import log 
from random import random

from head_to_head import head_to_head_read
from print_tree import print_tree
from tournament_bracket import bracket_builder, get_top_players
from winrate import winrate


def get_results(player_1, player_2):
    tag_rank, head_to_head = head_to_head_read("head_to_head.txt")
    high_seed = None
    low_seed = None
    if player_1["seed"] < player_2["seed"]:
        high_seed, low_seed = (player_1, player_2)
    else:
        high_seed, low_seed = (player_2, player_1)
    player_1_win_prob = winrate(high_seed, low_seed, tag_rank, head_to_head)
    random_val = random()
    print("{} v.s. {}".format(player_1["tag"], player_2["tag"]))
    print(player_1_win_prob)
    print(random_val)

    if random() <= player_1_win_prob:
        return (player_1, player_2)

    return (player_2, player_1)


def get_tree_levels(root):
    total_levels = []
    cur_level = [root]
    next_level = []

    while cur_level:
        for n in cur_level:
            if n.left:
                next_level.append(n.left)
            if n.right:
                next_level.append(n.right)
        total_levels.append(list(cur_level))
        cur_level = next_level
        next_level = []

    return total_levels


def simulate_winners(winners, losers_levels):
    winners_sequence = get_tree_levels(winners)
    cur_level_winners = []
    cur_level_losers = []
    cur_level = winners_sequence.pop()
    while len(cur_level) > 1:
        for cur_set in cur_level:
            set_winner, set_loser = get_results(cur_set.player_one,
                                                cur_set.player_two)
            cur_level_winners.append(set_winner)
            cur_level_losers.append(losers_levels)

        next_level = winners_sequence[-1] or []

        cur_level_winners.reverse()
        for next_set in next_level:
            next_set.player_one = cur_level_winners.pop()
            next_set.player_two = cur_level_winners.pop()

        losers_levels.append(list(cur_level_losers))
        cur_level = winners_sequence.pop()
        cur_level_winners = []
        cur_level_losers = []
    

if __name__ == "__main__":
    tournament_name = "get-on-my-level-2016"
    tournament_event ="melee-singles"
    top_players = get_top_players(tournament_name,
                                  tournament_event)
    winners_bracket, losers_bracket = bracket_builder(tournament_name,
                                                      tournament_event,
                                                      top_players)
    losers_levels = []
    simulate_winners(winners_bracket, losers_levels)
    print_tree(winners_bracket)

