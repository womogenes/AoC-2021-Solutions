with open("./day_07.in") as fin:
    raw_data = fin.read().strip().split(",")

data = [int(i) for i in raw_data]

ans = 1 << 60

max_pos = max(data)

for pos in range(max_pos):
    req = 0
    for i in data:
        dist = abs(i - pos)
        cost = dist * (dist + 1) // 2
        req += cost
    ans = min(ans, req)

print(ans)
