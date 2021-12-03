# Let's use proper bit operations now
with open("./day_03.in") as fin:
    data = fin.read().strip().split("\n")

# Determine number of bits
N = len(data[0])

data = [int(i, 2) for i in data]

# Find oxygen rating
o2_rem = data.copy()
pos = N - 1
while pos >= 0 and len(o2_rem) > 1:
    # Find the most common bit
    ones = sum([((x & (1 << pos)) >> pos) for x in o2_rem])
    zeros = len(o2_rem) - ones

    if zeros > ones:
        o2_rem = list(filter(lambda x: not (x & (1 << pos)), o2_rem))
    else:
        o2_rem = list(filter(lambda x: (x & (1 << pos)), o2_rem))

    pos -= 1

# Find co2 rating
co2_rem = data.copy()
pos = N - 1
while pos >= 0 and len(co2_rem) > 1:
    # Find the most common bit
    ones = sum([((x & (1 << pos)) >> pos) for x in co2_rem])
    zeros = len(co2_rem) - ones

    if zeros > ones:
        co2_rem = list(filter(lambda x: (x & (1 << pos)), co2_rem))
    else:
        co2_rem = list(filter(lambda x: not (x & (1 << pos)), co2_rem))

    pos -= 1


ans = o2_rem[0] * co2_rem[0]
print(ans)
