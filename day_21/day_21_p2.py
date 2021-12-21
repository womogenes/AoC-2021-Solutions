from functools import lru_cache

with open("./day_21.in") as fin:
    raw_data = fin.read().strip().split("\n")


p1 = int(raw_data[0][raw_data[0].index(": ")+2:])
p2 = int(raw_data[1][raw_data[1].index(": ")+2:])

freq = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}


def advance(pos, amount):
    return (pos + amount - 1) % 10 + 1


def regress(pos, amount):
    return (pos - amount - 1) % 10 + 1


@lru_cache(None)
def dp(pos, score, turn, init_pos):
    # How many ways are there to get to a given score, on given position, on given turn?
    if turn == 0:
        return 1 if (score == 0 and pos == init_pos) else 0

    if score <= 0:
        return 0

    ans = 0
    for amount in freq:
        if score - pos >= 21:
            continue

        dp_val = dp(regress(pos, amount),
                    score - pos, turn - 1, init_pos)
        ans += freq[amount] * dp_val

    return ans


# Number of ways for given to win
def count_wins(pos, other_pos, is_p1):
    ans = 0
    for end_pos in range(1, 11):
        for score in range(21, 31):
            for turn in range(40):
                for other_end_pos in range(1, 11):
                    for other_score in range(21):
                        ans += dp(end_pos, score, turn, pos) * \
                            dp(other_end_pos, other_score,
                               turn - is_p1, other_pos)

    return ans


p1 = count_wins(p1, p2, True)
p2 = count_wins(p2, p1, False)
print(max(p1, p2))
