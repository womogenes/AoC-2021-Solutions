with open("./day_09.in") as fin:
    raw_data = fin.read().strip().split("\n")
    map = [[int(i) for i in list(line)] for line in raw_data]

rows = len(map)
cols = len(map[0])

ans = 0
# Find low points
for row in range(rows):
    for col in range(cols):
        low = True
        for d in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            rr = row + d[0]
            cc = col + d[1]

            if not ((0 <= rr and rr < rows) and (0 <= cc and cc < cols)):
                continue

            if map[rr][cc] <= map[row][col]:
                low = False
                break

        if low:
            ans += map[row][col] + 1

print(ans)
