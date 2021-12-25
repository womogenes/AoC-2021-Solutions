import copy

with open("./day_25.in") as fin:
    raw_data = fin.read().strip()
    grid = [list(line) for line in raw_data.split("\n")]

rows = len(grid)
cols = len(grid[0])


def do_step(grid, c_type):
    # c_type is "v" or ">"
    new_grid = copy.deepcopy(grid)
    any_moved = False

    for row in range(rows):
        for col in range(cols):
            if c_type != grid[row][col]:
                continue

            if grid[row][col] == "v":
                dest = (row + 1) % rows, col
            else:
                dest = row, (col + 1) % cols

            if grid[dest[0]][dest[1]] == ".":
                any_moved = True
                new_grid[dest[0]][dest[1]] = grid[row][col]
                new_grid[row][col] = "."

    return new_grid, any_moved


step = 0
while True:
    grid, any_moved_e = do_step(grid, ">")
    grid, any_moved_s = do_step(grid, "v")
    step += 1
    if not (any_moved_s or any_moved_e):
        break

print(step)
