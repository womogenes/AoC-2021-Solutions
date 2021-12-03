with open("./day_03.in") as fin:
    data = fin.read().strip().split("\n")


N = len(data[0])  # Length of binary strings

# Find the rates
gamma_rate = [None] * N
epsilon_rate = [None] * N
for i in range(N):
    zeros = sum([data[j][i] == "0" for j in range(len(data))])
    ones = sum([data[j][i] == "1" for j in range(len(data))])
    if zeros > ones:
        gamma_rate[i] = "0"
        epsilon_rate[i] = "1"
    else:
        gamma_rate[i] = "1"
        epsilon_rate[i] = "0"

# Final answer
ans = int("".join(gamma_rate), 2) * int("".join(epsilon_rate), 2)
print(ans)
