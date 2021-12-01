with open("./day_01.in") as fin:
    data = [int(i) for i in fin.read().strip().split("\n")]

N = len(data)

count = 0  # Number of increasing depths

for i in range(1, N):
    if data[i] > data[i - 1]:
        count += 1

print(count)
