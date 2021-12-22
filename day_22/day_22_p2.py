from collections import defaultdict

with open("./day_22.in") as fin:
    raw_data = fin.read().strip().split("\n")

steps = []


def volume(bounds):
    # Compute volume of cuboid
    p = 1
    for b in bounds:
        assert b[1] >= b[0]
        p *= abs(b[1] - b[0]) + 1
    return p


def overlap(bounds1, bounds2):
    # Intersect two cubes to find a new cube!
    ans = []
    for b1, b2 in zip(bounds1, bounds2):
        if b1[1] < b2[0] or b2[1] < b1[0]:
            return None

        bounds = (max(b1[0], b2[0]), min(b1[1], b2[1]))
        ans.append(bounds)

    return tuple(ans)


for line in raw_data:
    parts = line.split(" ")
    switch = parts[0] == "on"
    bounds = []
    for axis in parts[1].split(","):
        axis = axis.split("..")
        bounds.append((int(axis[0][2:]), int(axis[1])))

    steps.append((switch, tuple(bounds)))


counts = defaultdict(int)
for i in range(len(steps)):
    switch, bounds = steps[i]

    new_counts = defaultdict(int)
    keys = set(counts.keys())
    for o_cube in keys:
        o_switch = counts[o_cube] > 0
        o = overlap(bounds, o_cube)
        if o == None:
            continue

        new_counts[o] -= counts[o_cube]  # Reset to 0

    if switch:
        new_counts[bounds] += 1

    for c in new_counts:
        counts[c] += new_counts[c]


ans = 0
for cube in counts:
    ans += volume(cube) * counts[cube]
print(ans)
