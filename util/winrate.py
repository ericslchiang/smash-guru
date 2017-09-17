from math import exp

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

    global_factor = 0.5 / (1 + exp(-(lo_seed - hi_seed)))
    h2h_factor = 0
    num_h2h_sets = hi_seed_set_win_lo_seed + lo_seed_set_win_hi_seed

    if num_h2h_sets > 0:
        h2h_factor = 0.5 * (hi_seed_set_win_lo_seed / num_h2h_sets)
        print("h2h: {}".format(h2h_factor))

    return global_factor + h2h_factor

