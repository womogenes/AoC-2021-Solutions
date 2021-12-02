with open("./day_02.in") as fin:
    data = fin.read().strip().split("\n")


def parse_line(line, prev_aim):
    cmd, amount = line.split(" ")
    amount = int(amount)
    if cmd == "forward":
        return (amount, amount * prev_aim, 0)
    elif cmd == "down":
        return (0, 0, amount)
    else:
        return (0, 0, -amount)


pos, depth, aim = 0, 0, 0

for line in data:
    dpos, ddepth, daim = parse_line(line, aim)
    pos += dpos
    depth += ddepth
    aim += daim

ans = pos * depth
print(ans)
