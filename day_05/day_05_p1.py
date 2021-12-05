import numpy as np

with open("./day_05.in") as fin:
    data = fin.read().strip().split("\n")


def parse_line(line):
    """
    Parse a line in the input
    """
    start, _, end = line.split(" ")
    start = [int(i) for i in start.split(",")]
    end = [int(i) for i in end.split(",")]
    return start, end


# Definitely not confusing variable naming
lines = [parse_line(line) for line in data]

# Discard points that aren't vertical or horizontal
lines = [li for li in lines
         if li[0][0] == li[1][0] or li[0][1] == li[1][1]]

# Find the boundaries of the grid
max_x = 0
max_y = 0
for li in lines:
    max_x = max(max_x, li[0][0], li[1][0])
    max_y = max(max_y, li[0][1], li[1][1])

cover = np.zeros((max_x + 1, max_y + 1))
for li in lines:
    start, end = li
    if start[0] == end[0]:
        bottom = min(start[1], end[1])
        top = max(start[1], end[1])
        for y in range(bottom, top + 1):
            cover[start[0]][y] += 1

    else:
        assert start[1] == end[1]
        left = min(start[0], end[0])
        right = max(start[0], end[0])
        for x in range(left, right + 1):
            cover[x][start[1]] += 1


# Find out how many points are covered more than once
ans = 0
for count in cover.flatten():
    ans += count >= 2

print(cover.transpose())
print(ans)
