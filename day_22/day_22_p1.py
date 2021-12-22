import numpy as np

with open("./day_22.in") as fin:
    raw_data = fin.read().strip().split("\n")


def within_bounds(x_range, y_range, z_range):
    for b in x_range, y_range, z_range:
        if not (0 <= b[0] and b[1] <= 100):
            return False
    return True


steps = []

for line in raw_data:
    parts = line.split(" ")
    switch = parts[0] == "on"
    bounds = []
    for axis in parts[1].split(","):
        axis = axis.split("..")
        bounds.append((int(axis[0][2:]) + 50, int(axis[1]) + 50))

    steps.append((switch, bounds))

grid = np.zeros((101, 101, 101), dtype=bool)

for switch, bounds in steps:
    x_range, y_range, z_range = bounds
    if not within_bounds(x_range, y_range, z_range):
        continue

    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            for z in range(z_range[0], z_range[1] + 1):
                grid[x, y, z] = switch


ans = 0
for x in grid.flatten():
    ans += x
print(ans)
