with open("./day_21.in") as fin:
    raw_data = fin.read().strip().split("\n")


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0

    def advance(self, die):
        self.pos += die.roll()
        self.pos = (self.pos - 1) % 10 + 1
        self.score += self.pos

    def win(self):
        return self.score >= 1000


class Dice:
    def __init__(self):
        self.val = 1
        self.rolls = 0

    def roll(self, times=3):
        s = 0
        for _ in range(times):
            s += self.val
            self.val += 1
        self.rolls += times
        return s


p1 = Player(int(raw_data[0][raw_data[0].index(": ")+2:]))
p2 = Player(int(raw_data[1][raw_data[1].index(": ")+2:]))

d = Dice()

while True:
    p1.advance(d)
    if p1.win():
        ans = p2.score * d.rolls
        break

    p2.advance(d)
    if p2.win():
        ans = p1.score * d.rolls
        break

print(ans)
