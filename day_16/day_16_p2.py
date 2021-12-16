with open("./day_16.in") as fin:
    raw_data = fin.read().strip()

data = bin(int(raw_data, base=16))[2:]
data = data.zfill(-(-len(data)//4) * 4)


def operate(typeID, values):
    if typeID == 0:
        return sum(values)

    if typeID == 1:
        p = 1
        for v in values:
            p *= v
        return p

    if typeID == 2:
        return min(values)

    if typeID == 3:
        return max(values)

    if typeID == 5:
        assert len(values) == 2
        return int(values[0] > values[1])

    if typeID == 6:
        assert len(values) == 2
        return int(values[0] < values[1])

    if typeID == 7:
        assert len(values) == 2
        return int(values[0] == values[1])


def parse(i, j=-1):
    """
    Parse the data
      - starting at index i
      - ending at j
      - with rem packets left

    Return
      - value of current packet
      - where the next packet starts
    """
    if i == j:
        return None, None

    # Not useful bits anymore
    if i > len(data) - 4:
        return None, None

    ver = int(data[i:i+3], base=2)
    typeID = int(data[i+3:i+6], base=2)

    # Literal packet
    if typeID == 4:
        i += 6
        num_str = ""
        end = False
        while not end:
            if data[i] == "0":
                # Last packet
                end = True

            num_str += data[i+1:i+5]
            i += 5

        val = int(num_str, base=2)
        return val, i

    # Operator packet
    sub_packs = []
    next_start = None  # A value to return

    lenID = data[i+6]
    if lenID == "0":
        # 15 bits representing how many bits are inside
        num_bits = int(data[i+7:i+22], base=2)
        end = i + 22 + num_bits
        index = i + 22
        prev_index = None
        while index != None:
            prev_index = index
            x, index = parse(index, j=end)
            sub_packs.append(x)
        sub_packs = sub_packs[:-1]  # Remove last None
        next_start = prev_index

    else:
        # 11 bits representing how many packets are inside
        rem_sub_packs = int(data[i+7:i+18], base=2)
        index = i + 18
        while rem_sub_packs > 0:
            x, index = parse(index)
            rem_sub_packs -= 1
            sub_packs.append(x)
        next_start = index

    # Process the operations
    return operate(typeID, sub_packs), next_start


ans = parse(0)[0]
print(ans)
