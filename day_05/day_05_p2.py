from os import link
import numpy as np

with open("./day_05.in") as fin:
    data = fin.read().strip().split("\n")


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def parse_line(line):
    """
    Parse a line in the input
    """
    start, _, end = line.split(" ")
    start = [int(i) for i in start.split(",")]
    end = [int(i) for i in end.split(",")]

    # Direction vector for looping purposes
    direc = [sign(end[0] - start[0]), sign(end[1] - start[1])]

    return start, end, direc


# Definitely not confusing variable naming
lines = [parse_line(line) for line in data]

# Find the boundaries of the grid
max_x = 0
max_y = 0
for li in lines:
    max_x = max(max_x, li[0][0], li[1][0])
    max_y = max(max_y, li[0][1], li[1][1])

cover = np.zeros((max_x + 1, max_y + 1))
for li in lines:
    start, end, direc = li
    p = start
    while p != end:
        cover[p[0], p[1]] += 1
        p[0] += direc[0]
        p[1] += direc[1]
    cover[end[0]][end[1]] += 1


# Find out how many points are covered more than once
ans = 0
for count in cover.flatten():
    ans += count >= 2

cover.transpose()

for i in cover:
    print("".join([str(int(x)) if x > 0 else "." for x in i]))

print(ans)
