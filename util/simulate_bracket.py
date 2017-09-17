from math import log 
from random import random

from head_to_head import head_to_head_read
from print_tree import print_tree
from tournament_bracket import bracket_builder, get_top_players
from tree_node import TreeNode
from winrate import winrate


def get_results(player_1, player_2):
    tag_rank, head_to_head = head_to_head_read("util/head_to_head.txt")
    high_seed = None
    low_seed = None
    if player_1["seed"] < player_2["seed"]:
        high_seed, low_seed = (player_1, player_2)
    else:
        high_seed, low_seed = (player_2, player_1)
    player_1_win_prob = winrate(high_seed, low_seed, tag_rank, head_to_head)
    random_val = random()

    # print("{} v.s. {}".format(player_1["tag"], player_2["tag"]))
    # print(player_1_win_prob)
    # print(random_val)

    if random() <= player_1_win_prob:
        return (high_seed, low_seed)

    return (low_seed, high_seed)


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

def simulate_bracket(bracket, losers_levels, placings=None):
    bracket_sequence = get_tree_levels(bracket)
    level_winners = []
    level_losers = []
    level = bracket_sequence.pop()
    
    while len(level) > 1:
        for cur_set in level:
            set_winner, set_loser = get_results(cur_set.player_one,
                                                cur_set.player_two)
            if placings is not None:
                placings.append(set_loser)
            level_winners.append(set_winner)
            level_losers.append(set_loser)

        if placings is None:
            # if winners bracket, keep track of all losing
            # players by bracket level.
            losers_levels.append(list(level_losers))
            level = bracket_sequence.pop()

            # setup players for next bracket level.
            level_winners.reverse()
            for next_set in level:
                next_set.player_one = level_winners.pop()
                next_set.player_two = level_winners.pop()

        else:
            # if losers bracket, use losers from winners bracket to refill
            # the bracket once.
            level = filter(lambda cur_set: not cur_set.has_simmed,
                           level)
            for cur_set in level:
                cur_set.has_simmed = True

            level_winners.reverse()
            losers_pool_one = level_winners
            losers_pool_two = None
            # if all sets have been reused already, use next bracket sequence
            # and take both loser candidates from those who just won
            # from losers, instead of losers from winners.

            if level:
                losers_pool_two = losers_levels.pop()
            else:
                level = bracket_sequence.pop()
                losers_pool_two = level_winners

            # setup players fro next bracket level.

            for next_set in level:
                next_set.player_one = losers_pool_one.pop()
                next_set.player_two = losers_pool_two.pop()

        level_winners = []
        level_losers = []

def simulate_winners(winners, losers_levels):
    simulate_bracket(winners, losers_levels)

def simulate_losers(losers, losers_levels, placings):
    # reuse the bracket once in losers to retain the tree structre
    simulate_bracket(losers, losers_levels, placings)
    
    
def simulate_tournament(winners, losers):
    placings = []
    losers_levels = []
    
    simulate_winners(winners, losers_levels)
    losers_levels.reverse()

    simulate_losers(losers, losers_levels, placings)

    grand_finals = TreeNode()
    losers_finals = TreeNode()

    wf_winner, wf_loser = get_results(winners.player_one, winners.player_two)

    ls_winner, ls_loser = get_results(losers.player_one, losers.player_two)
    placings.append(ls_loser)

    losers_finals.player_one = wf_loser
    losers_finals.player_two = ls_winner
    lf_winner, lf_loser = get_results(losers_finals.player_one,
                                      losers_finals.player_two)
    placings.append(lf_loser)

    grand_finals.player_one = wf_winner
    grand_finals.player_two = lf_winner

    gf_winner, gf_loser = get_results(grand_finals.player_one,
                                      grand_finals.player_two)

    if not gf_winner == grand_finals.player_one:
        gf_winner, gf_loser = get_results(grand_finals.player_one,
                                          grand_finals.player_two)
    placings.append(gf_loser)
    placings.append(gf_winner)

    return placings


if __name__ == "__main__":
    tournament_name = "get-on-my-level-2016"
    tournament_event ="melee-singles"
    top_players = get_top_players(tournament_name,
                                  tournament_event)
    winners_bracket, losers_bracket = bracket_builder(tournament_name,
                                                      tournament_event,
                                                      top_players)
    placings = simulate_tournament(winners_bracket, losers_bracket)
    placings.reverse()

    placings = map(lambda player: player["tag"], placings)
    for player in placings:
        print(player)

    # print_tree(winners_bracket)
    # print_tree(losers_bracket)

