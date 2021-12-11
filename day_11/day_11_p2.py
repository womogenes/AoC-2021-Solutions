import numpy as np
from itertools import product

with open("./day_11.in") as fin:
    raw_data = fin.read().strip()
data = np.array([[int(x) for x in list(i)]
                for i in raw_data.split("\n")], dtype=int)

ans = 0

N = len(data)

octos = data

step = 1

while True:
    flashed = np.zeros((N, N), dtype=bool)

    for i, j in product(range(N), repeat=2):
        octos[i, j] += 1

    while True:
        keep_going = False

        # Make octos flash!
        change = np.zeros((N, N), dtype=int)

        for i, j in product(range(N), repeat=2):
            if not flashed[i, j] and octos[i, j] > 9:

                ans += 1
                flashed[i, j] = True
                keep_going = True

                for di, dj in product(range(-1, 2), repeat=2):
                    if di == dj == 0:
                        continue

                    ii = i + di
                    jj = j + dj

                    if not (0 <= ii < N and 0 <= jj < N):
                        continue

                    change[ii, jj] += 1

        octos += change

        # print("Change:")
        # pprint(change)

        if not keep_going:
            break

    flashed_count = 0
    for i, j in product(range(N), repeat=2):
        if flashed[i, j]:
            flashed_count += 1
            octos[i, j] = 0

    if flashed_count == N * N:
        break

    step += 1

print(step)
