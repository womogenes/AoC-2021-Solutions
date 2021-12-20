from itertools import product

with open("./day_20.in") as fin:
    raw_data = fin.read().strip().split("\n")

algo = raw_data[0]
image_raw = raw_data[2:]

# Represent the image as a set of light points
image = set()

for row in range(len(image_raw)):
    for col in range(len(image_raw[0])):
        if image_raw[row][col] == "#":
            image.add((row, col))


def get_bounds(image):
    min_row = 1 << 60
    max_row = -(1 << 60)
    min_col = 1 << 60
    max_col = -(1 << 60)
    for row, col in image:
        min_row, max_row = min(min_row, row), max(max_row, row)
        min_col, max_col = min(min_col, col), max(max_col, col)

    return min_row, max_row, min_col, max_col


def print_image(image):
    min_row, max_row, min_col, max_col = get_bounds(image)

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if (row, col) in image:
                print("#", end="")
            else:
                print(".", end="")
        print()


def enhance(image, bounds):
    # Get the bounds first
    output = set()
    min_row, max_row, min_col, max_col = bounds

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            new_pix = ""  # Binary string

            for drow in range(-1, 2):
                for dcol in range(-1, 2):
                    rr = row + drow
                    cc = col + dcol
                    new_pix += "1" if (rr, cc) in image else "0"

            if algo[int(new_pix, base=2)] == "#":
                output.add((row, col))

    return output


min_x, max_x, min_y, max_y = get_bounds(image)
min_x -= 200
max_x += 200
min_y -= 200
max_y += 200

for i in range(50):
    image = enhance(image, (min_x, max_x, min_y, max_y))
    min_x += 3
    max_x -= 3
    min_y += 3
    max_y -= 3


print(len(image))
