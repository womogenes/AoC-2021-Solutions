with open("./day_17.in") as fin:
    raw_data = fin.read().strip()

data = raw_data[len("target area: x="):]
data = data.split(", y=")
x_range = (
    int(data[0][:data[0].index("..")]),
    int(data[0][data[0].index("..")+2:])
)
y_range = (
    int(data[1][:data[1].index("..")]),
    int(data[1][data[1].index("..")+2:])
)

target = (x_range, y_range)


def iterate(pos, vel):
    """
    Return new position and new velocity
    """
    new_pos = [0, 0]
    new_vel = [0, 0]

    new_pos[0] = pos[0] + vel[0]
    new_pos[1] = pos[1] + vel[1]

    new_vel[1] = vel[1] - 1
    if vel[0] > 0:
        new_vel[0] = vel[0] - 1
    if vel[0] < 0:
        new_vel[0] = vel[0] + 1

    return new_pos, new_vel


def is_within(pos, target):
    return (target[0][0] <= pos[0] <= target[0][1]) \
        and (target[1][0] <= pos[1] <= target[1][1])


def is_past(pos, vel, target):
    if vel[0] > 0 and pos[0] > target[0][1]:
        return True
    if vel[0] < 0 and pos[0] < target[0][0]:
        return True
    if vel[1] < 0 and pos[1] < target[1][0]:
        return True
    return False


def does_hit(vel, target):
    """
    target = [x_range, y_range]
    """
    pos = (0, 0)
    while not is_past(pos, vel, target):
        max_y = max(max_y, pos[1])
        if is_within(pos, target):
            return True
        pos, vel = iterate(pos, vel)

    return False


# Test out a bunch of stuff
ans = 0

# This is the limit of the y velocity
max_yv = abs(target[1][0])

yv = max_yv
while yv >= target[1][0]:
    done = False
    for xv in range(-100, 101):
        works = does_hit((xv, yv), target)
        if works:
            ans += 1
            done = True

    yv -= 1

print(ans)
