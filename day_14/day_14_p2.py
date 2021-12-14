import string
from collections import defaultdict
import copy

with open("./day_14.in") as fin:
    raw_data = fin.read().strip().split("\n")

template = raw_data[0]
rules = [line.split(" -> ") for line in raw_data[2:]]

# Modify the template
freqs = defaultdict(int)
for i in range(len(template) - 1):
    freqs[template[i:i + 2]] += 1

elements = string.ascii_uppercase


def replace(freqs):
    new_freqs = copy.copy(freqs)
    for pair in freqs:
        for start, end in rules:
            if pair == start:
                occs = freqs[pair]
                new_freqs[pair] -= occs
                new_freqs[pair[0] + end] += occs
                new_freqs[end + pair[1]] += occs
                break

    return new_freqs


for i in range(40):
    freqs = replace(freqs)

# Count each element
count = defaultdict(int)
for pair in freqs:
    count[pair[0]] += freqs[pair]
    count[pair[1]] += freqs[pair]

count[template[0]] += 1
count[template[-1]] += 1

count_vals = [c[1] // 2 for c in count.items()]

ans = max(count_vals) - min(count_vals)
print(ans)
