"""
Note: This doesn't automatically parse the input file!
      You must parse it yourself.
      Watch this video for details: https://youtu.be/Eswmo7Y7C4U
"""

from itertools import product

with open("./day_24.in") as fin:
    raw_data = fin.read().strip().split("\n\n")[4:5]

steps = [6, 12, 8, None, 7, 12, 2, None, 4, None, None, None, None, None]
required = [None, None, None, 11, None, None, None, 7, None, 6, 10, 15, 9, 0]

input_space = product(range(1, 10), repeat=7)


def works(digits):
    z = 0
    res = [0] * 14

    digits_idx = 0

    for i in range(14):
        increment, mod_req = steps[i], required[i]

        if increment == None:
            assert mod_req != None
            res[i] = ((z % 26) - mod_req)
            z //= 26
            if not (1 <= res[i] <= 9):
                return False

        else:
            assert increment != None
            z = z * 26 + digits[digits_idx] + increment
            res[i] = digits[digits_idx]
            digits_idx += 1

    return res


for digits in input_space:
    res = works(digits)
    if res:
        print("".join([str(i) for i in res]))
        break
