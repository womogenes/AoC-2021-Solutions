from collections import defaultdict, deque
from pprint import pprint


def is_small(cave):
    return cave.islower()


with open("./day_12.in") as fin:
    raw_data = fin.read().strip()
data = [i.split("-") for i in raw_data.split("\n")]


adj = defaultdict(list)

for a, b in data:
    adj[a].append(b)
    adj[b].append(a)


# Number of paths
global ans
ans = 0

# Do some DFS!
visited = defaultdict(int)


def dfs(cave):
    global ans

    if cave == "end":
        ans += 1
        return

    if is_small(cave):
        visited[cave] += 1

        # Check if this cave is good to go
        more_than_once = 0  # How many small caves are visited more than once
        for small in visited:
            more_than_once += visited[small] > 1

            # No small cave can be visited more than twice
            if visited[small] > 2:
                visited[cave] -= 1
                return

        if more_than_once > 1:
            visited[cave] -= 1
            return

    # Add all neighbors to queue
    for nbr in adj[cave]:
        if nbr == "start":
            # Don't explore start cave again
            continue
        dfs(nbr)

    # At the end, remove this from the DFS
    if is_small(cave):
        visited[cave] -= 1


dfs("start")

print(ans)
