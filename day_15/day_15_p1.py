import heapq
from collections import defaultdict

with open("./day_15.in") as fin:
    raw_data = fin.read().strip()
map = [[int(i) for i in line] for line in raw_data.split("\n")]

N = len(map)
M = len(map[0])

cost = defaultdict(int)

pq = [(0, 0, 0)]
heapq.heapify(pq)
visited = set()

while len(pq) > 0:
    c, row, col = heapq.heappop(pq)

    if (row, col) in visited:
        continue
    visited.add((row, col))

    cost[(row, col)] = c

    if row == N - 1 and col == M - 1:
        break

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        rr = row + dr
        cc = col + dc
        if not (0 <= rr < N and 0 <= cc < M):
            continue

        heapq.heappush(pq, (c + map[rr][cc], rr, cc))


print(cost[(N - 1, M - 1)])
