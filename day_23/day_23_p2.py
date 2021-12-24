from pprint import pprint
import heapq
from collections import defaultdict

with open("./day_23.in") as fin:
    raw_data = fin.read().strip().split("\n")

hallway = raw_data[1][1:12]
row_1 = raw_data[2][3:10:2]
row_2 = "DCBA" if len(raw_data) == 5 else raw_data[3][3:10:2]
row_3 = "DBAC" if len(raw_data) == 5 else raw_data[4][3:10:2]
row_4 = raw_data[3 if len(raw_data) == 5 else 5][3:10:2]

"""
The state of an amphipod can be represented with a tuple:
    (loc, room, depth)
Assume all amphipods have fully moved
Room is one of 2, 4, 6, 8

State is given as
    (apods, cost)
"""


def print_apods(apods):
    grid = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  # """.strip()
    grid = [list(line) for line in grid.split("\n")]
    for i, state in enumerate(apods):
        loc, room, depth = state
        c = "ABCD"[i//4]
        if loc != -1:
            grid[1][loc + 1] = c
        else:
            grid[depth + 1][room + 1] = c

    print("\n".join(["".join(line) for line in grid]))
    print()


def any_blocking(apods, idx, dest):
    # Check if any amphipods between a pods[idx] and dest room
    assert len(apods) == 16

    hall_loc, room, _ = apods[idx]
    assert hall_loc == -1 or room == -1
    loc = max(hall_loc, room)

    for j in range(16):
        if j == idx or apods[j][0] == -1:
            continue

        o_loc = apods[j][0]
        assert loc != o_loc

        if (dest <= o_loc <= loc) or (loc <= o_loc <= dest):
            return True

    return False


def get_room(apods, target_room):
    # Return list of amphipods in given room
    assert target_room in [2, 4, 6, 8]
    res = [-1] * 4

    for i, apod in enumerate(apods):
        type = i // 4
        loc, room, depth = apod
        if room != -1:
            assert loc == -1 and depth != -1
            if room != target_room:
                continue
            res[4 - depth] = type

    # Make sure it's filled from the bottom up
    i = 0
    while i < 4 and res[i] != -1:
        i += 1
    while i < 4:
        try:
            assert res[i] == -1
        except:
            print_apods(apods)
            print(target_room, res)

            print("\nparent:")
            print_apods(breadcrumbs[apods])
            raise ValueError()

        i += 1

    return res


def children(state):
    # Compute all next states from given state
    cost, apods = state
    assert len(apods) == 16

    # AAaaaaaa assert
    for room in [2, 4, 6, 8]:
        get_room(apods, room)

    for i, apod in enumerate(apods):
        type = i // 4
        loc, room, depth = apod

        assert not loc in [2, 4, 6, 8]

        # Is this amphipod settled in?
        if loc == -1:
            assert room != -1
            if room == (type + 1) * 2:
                if depth == 4:
                    continue

                # print(f"  {room}, {get_room(apods, room)[:4-depth]}")
                if get_room(apods, room)[:4-depth] == [type] * (4 - depth):
                    continue

        # In the hallway
        out_cost = 0 if room == -1 else depth
        practical_loc = max(loc, room)

        # Try to move into a room next turn
        dest_room = (type + 1) * 2

        # If you are in a room and wish to go out, check first if you can actually get out
        good = True
        if room != -1 and depth > 1:
            assert loc == -1
            blocking = False

            for j in range(16):
                if j == i:
                    continue

                if apods[j][1] == room and apods[j][2] < depth:
                    blocking = True
                    break

            good = not blocking

        if good:
            # Any foreigners in this room?
            foreigners = False
            for j in range(16):
                if j // 4 == type or apods[j][1] == -1:
                    # Is self, or is of same type, or not in dest room
                    continue

                if apods[j][1] == dest_room:
                    foreigners = True
                    break

            if not foreigners:
                target_depth = 4
                room_list = get_room(apods, dest_room)

                # IF THERE IS AN INDEX ERROR IN THIS LOOP
                # Then something went wrong
                # Get target depth for target room
                while room_list[4 - target_depth] != -1:
                    assert room_list[4 - target_depth] == type
                    target_depth -= 1

                # There is open room
                if not any_blocking(apods, i, dest_room):
                    cost_to_move = pow(
                        10, type) * (abs(practical_loc - dest_room) + target_depth + out_cost)
                    apods_copy = list(apods)
                    apods_copy[i] = (-1, dest_room, target_depth)
                    yield cost + cost_to_move, tuple(apods_copy)

        # In a room
        if room == -1:
            assert loc != -1
            continue

        assert room != -1 and depth != -1 and loc == -1

        # Check if anyone's blocking in the current room
        if depth > 1:
            blocking = False
            for j in range(16):
                if j == i:
                    continue

                if apods[j][1] == room and apods[j][2] < depth:
                    blocking = True
                    break

            if blocking:
                continue

        # Go into the hallway?
        for dest_loc in [0, 1, 3, 5, 7, 9, 10]:
            cost_to_move = pow(10, type) * (abs(room - dest_loc) + (depth))

            if any_blocking(apods, i, dest_loc):
                continue

            apods_copy = list(apods)
            apods_copy[i] = (dest_loc, -1, -1)
            yield cost + cost_to_move, tuple(apods_copy)

        # And that's it!


def detect_end(apods):
    for type in range(4):
        if get_room(apods, (type + 1) * 2) != [type] * 4:
            return False

    return True


start_apods = [None] * 16
type_counter = [0, 0, 0, 0]

# Parse hallway
for loc in range(11):
    if hallway[loc] == ".":
        continue
    type = "ABCD".index(hallway[loc])
    start_apods[type*4 + type_counter[type]] = (loc, -1, -1)
    type_counter[type] += 1

# Parse rooms
for row, depth in [(row_1, 1), (row_2, 2), (row_3, 3), (row_4, 4)]:
    for i in range(4):
        if row[i] == ".":
            continue
        type = "ABCD".index(row[i])
        start_apods[type*4 + type_counter[type]] = (-1, (i*2)+2, depth)
        type_counter[type] += 1

start_state = 0, tuple(start_apods)

""" print_apods(start_state[1])
print()

for child in children(start_state):
    print("child:", child[0])
    print_apods(child[1])
    print(detect_end(child[1]))
exit() """

breadcrumbs = defaultdict(tuple)

visited = set()
cost = defaultdict(int)

end_apods = None
ans = None

# Dijkstra's!
pq = [start_state]
while len(pq) > 0:
    cur_cost, cur_apods = heapq.heappop(pq)

    if cur_apods in visited:
        continue
    visited.add(cur_apods)

    cost[cur_apods] = cur_cost
    if detect_end(cur_apods):
        ans = cur_cost
        end_apods = cur_apods
        break

    for next_state in children((cur_cost, cur_apods)):
        if next_state[1] in visited:
            continue

        breadcrumbs[next_state[1]] = cur_apods
        heapq.heappush(pq, next_state)


cur_apods = end_apods
while breadcrumbs[cur_apods] != tuple():
    print(cost[cur_apods])
    print_apods(cur_apods)
    cur_apods = breadcrumbs[cur_apods]

print(ans)
