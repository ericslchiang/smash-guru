def head_to_head_read(input_file):
    tag_rank = {}
    head_to_head = None
    with open(input_file, "rb") as f:
        for i, line in enumerate(f):
            tokens = line.split("|")
            if i == 0:
                tag_rank = {tag.lower(): (j+1) for j, tag in enumerate(tokens)}
                num_players = len(tokens)
                head_to_head = [[0 for i in xrange(num_players)]
                               for i in xrange(num_players)]
            else:
                player_1 = i - 1
                for player_2, token in enumerate(tokens):
                    if token.strip():
                        head_to_head[player_1][player_2] = int(token)
        return (tag_rank, head_to_head)

if __name__ == "__main__":
    tag_rank, head_to_head = head_to_head_read("head_to_head.txt")
    print tag_rank
    print head_to_head
    mang0_rank = tag_rank["mang0"]
    leffen_rank = tag_rank["leffen"]
    print head_to_head[mang0_rank][leffen_rank]
    print head_to_head[leffen_rank][mang0_rank]
