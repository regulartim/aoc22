import time

begin = time.time()

###

with open("input.txt") as file:
	inventories = file.read().split("\n\n")[:-1]

calorie_sums = [sum(int(item) for item in inventory.split()) for inventory in inventories]
calorie_sums.sort(reverse=True)

print(f"Part 1: {calorie_sums[0]}")
print(f"Part 2: {sum(calorie_sums[:3])}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
