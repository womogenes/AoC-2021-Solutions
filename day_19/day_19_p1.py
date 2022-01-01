from functools import lru_cache
from itertools import combinations
from collections import defaultdict

with open("./day_19.in") as fin:
    raw_data = fin.read().strip()
    raw_data = raw_data.split("\n")

"""
Game plan:
  - Function that generates all permutations of a set of 3D points (or vectors)
  - Keep track of a relative offsets between scanners
  - Keep track of orientations of scanners

  - Consider all pairs of scanners
      * Find whether we can piece them together
      * If we can, use beacon locations to find offsets and rotations
"""

# Parse some input
scanners = []
i = 0
while i < len(raw_data):
    beacons = []
    while i < len(raw_data) and len(raw_data[i]) > 0:
        if "--- scanner" in raw_data[i]:
            i += 1
            continue
        beacons.append(tuple([int(i)
                       for i in raw_data[i].split(",")]))
        i += 1
    scanners.append(tuple(sorted(beacons)))
    i += 1


@lru_cache(None)
def inv(rot):
    a = rotations((1, 2, 3))[rot]
    for inv_rot in range(24):
        if rotations(a)[inv_rot] == (1, 2, 3):
            return inv_rot


@lru_cache(None)
def compose(rot1, rot2):
    a = rotations(rotations((1, 2, 3))[rot1])[rot2]
    for comp_rot in range(24):
        if rotations((1, 2, 3))[comp_rot] == a:
            return comp_rot


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def neg(a):
    return (-a[0], -a[1], -a[2])


def mag(a):
    return a[0]**2 + a[1]**2 + a[2]**2


@lru_cache(None)
def rotations(point):
    # https://i.imgur.com/Ff1vGT9.png
    x, y, z = point
    return [
        (x, y, z), (x, z, -y), (x, -y, -z), (x, -z, y),
        (-x, -y, z), (-x, z, y), (-x, y, -z), (-x, -z, -y),
        (y, z, x), (y, x, -z), (y, -z, -x), (y, -x, z),
        (-y, -z, x), (-y, x, z), (-y, z, -x), (-y, -x, -z),
        (z, x, y), (z, y, -x), (z, -x, -y), (z, -y, x),
        (-z, -x, y), (-z, y, x), (-z, x, -y), (-z, -y, -x)
    ]


def hash(a):
    # Absolute value-ize and sort components
    return tuple(sorted([abs(x) for x in a]))


def offset_set(beacons):
    # Return set of relative offsets between beacons
    res = set()
    for a, b in combinations(beacons, r=2):
        res.add(sub(a, b))
    return res


@lru_cache(None)
def distance_set(beacons):
    # beacons should be a tuple
    return set([hash(v) for v in offset_set(beacons)])


def might_have_overlap(a, b):
    # Determine whether two scanners might overlap based on hashes only
    # (misleading naming)
    if len(set.intersection(distance_set(a), distance_set(b))) >= 66:
        return True
    return False


def orient(a, b, base_index, rots):
    # base_index is the index of some beacon in _a_ that can be aligned
    # rotations is 2 possible rotations (inverses of each other) that we should try
    a_set = set(a)

    for rot in rots:
        other_beacons = tuple([rotations(beacon)[rot] for beacon in b])
        for other_base in other_beacons:
            translate = sub(a[base_index], other_base)
            other_beacons_translated = set(
                [add(beacon, translate) for beacon in other_beacons])

            # See if there's a line-up
            if len(set.intersection(a_set, other_beacons_translated)) >= 12:
                # Woo
                return translate, rot

    return None


def have_overlap(a, b):
    # Actually determine if scanners have overlap
    if not might_have_overlap(a, b):
        return False

    for i, j in combinations(range(len(a)), r=2):
        for k, m in combinations(range(len(b)), r=2):
            da = sub(a[i], a[j])
            db = sub(b[k], b[m])
            if not hash(da) == hash(db):
                continue

            # Determine the rotation and offset
            rots = []

            rot_db = rotations(db)
            for r in range(24):
                if rot_db[r] == da:
                    rots.append(r)
                    break

            # Try mirrored
            db = neg(db)
            rot_db = rotations(db)
            for r in range(24):
                if rot_db[r] == da:
                    rots.append(r)
                    break

            if len(rots) == 0:
                continue

            return orient(a, b, i, rots)

    return False


adj = defaultdict(list)
for i in range(len(scanners)):
    for j in range(i + 1, len(scanners)):
        x = have_overlap(scanners[i], scanners[j])
        if x:
            adj[i].append((j, x[0], x[1]))
            adj[j].append((i, rotations(neg(x[0]))[inv(x[1])], inv(x[1])))


# DFS time!
beacons = set()

stack = [(0, (0, 0, 0), 0)]
visited = set()
while len(stack) > 0:
    node, trans, rot = stack.pop()

    if node in visited:
        continue
    visited.add(node)

    # Add these beacons
    cur_beacons = [add(rotations(beacon)[rot], trans)
                   for beacon in scanners[node]]

    for b in cur_beacons:
        beacons.add(b)

    for nbr in adj[node]:
        if nbr[0] in visited:
            continue
        new_trans = add(trans, rotations(nbr[1])[rot])
        new_rot = compose(nbr[2], rot)
        stack.append((nbr[0], new_trans, new_rot))

print(len(beacons))
