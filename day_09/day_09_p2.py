import numpy as np

with open("./day_09.in") as fin:
    raw_data = fin.read().strip().split("\n")
    map = [[int(i) for i in list(line)] for line in raw_data]

rows = len(map)
cols = len(map[0])

low = []
cur_id = 1
ids = np.zeros((rows, cols), dtype=int)

# Find low points
for row in range(rows):
    for col in range(cols):
        is_low = True
        for d in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            rr = row + d[0]
            cc = col + d[1]

            if not ((0 <= rr and rr < rows) and (0 <= cc and cc < cols)):
                continue

            if map[rr][cc] <= map[row][col]:
                is_low = False
                break

        if is_low:
            low.append((row, col))

# Do some DFS
for row, col in low:
    stack = [(row, col)]
    visited = set()
    while len(stack) > 0:
        row, col = stack.pop()

        if (row, col) in visited:
            continue
        visited.add((row, col))

        ids[row, col] = cur_id

        for d in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            rr = row + d[0]
            cc = col + d[1]

            if not ((0 <= rr and rr < rows) and (0 <= cc and cc < cols)):
                continue

            if map[rr][cc] == 9:
                continue

            stack.append((rr, cc))

    cur_id += 1

# Find the sizes of biggest basins
sizes = [0] * cur_id

for x in ids.flatten():
    sizes[x] += 1
sizes = sizes[1:]

sizes.sort()
print(sizes[-1] * sizes[-2] * sizes[-3])
