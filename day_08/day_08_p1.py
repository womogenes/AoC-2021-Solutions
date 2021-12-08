with open("./day_08.in") as fin:
    raw_data = fin.read().strip().split("\n")
    data = [line[line.index("|") + 2:].split(" ") for line in raw_data]

good = [2, 4, 3, 7]

ans = 0
for output in data:
    for digit in output:
        if len(digit) in good:
            ans += 1

print(ans)
