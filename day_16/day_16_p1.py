with open("./day_16.in") as fin:
    raw_data = fin.read().strip()

data = bin(int(raw_data, base=16))[2:]
data = data.zfill(-(-len(data)//4) * 4)


def parse(packet, count=-1):
    """
    Parse a packet (or several, concatenated together)
    """
    if packet == "" or int(packet) == 0:
        return 0

    if count == 0:
        return parse(packet, count=-1)

    ver = int(packet[0:3], base=2)
    tID = int(packet[3:6], base=2)

    if tID == 4:
        # Literal packet
        i = 6
        num_str = ""
        end = False
        while not end:
            if packet[i] == "0":
                # Last packet
                end = True

            num_str += packet[i+1:i+5]
            i += 5

        val = int(num_str, base=2)
        return ver + parse(packet[i:], count-1)

    # Otherwise it's an operator
    len_ID = packet[6]
    if len_ID == "0":
        # 15 bits representing how many bits are inside
        num_bits = int(packet[7:22], base=2)
        return ver + parse(packet[22:22+num_bits], -1) + parse(packet[22+num_bits:], count-1)

    else:
        # 11 bits representing how many packets are inside
        num_packs = int(packet[7:18], base=2)
        return ver + parse(packet[18:], count=num_packs)


ans = parse(data)
print(ans)
