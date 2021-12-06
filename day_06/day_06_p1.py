with open("./day_06.in") as fin:
    raw_data = fin.read().strip().split(",")
    clocks = [int(i) for i in raw_data]


# After 80 days, something like 11 cycles will have gone by
# That's a growth rate of more than 2000!
# We can probably still brute force this
days = 80

for _ in range(days):
    n = len(clocks)
    for i in range(n):
        if clocks[i] == 0:
            clocks[i] = 6
            clocks.append(8)
        else:
            clocks[i] -= 1

ans = len(clocks)
print(ans)
