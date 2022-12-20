import re
import time

begin = time.time()

###

def dfs(state: tuple, cache: dict, blp: tuple, upper: tuple, next_bot_type: int) -> int:
	global best

	if state in cache:
		return cache[state]

	time_left, stock, robots = state

	if time_left == 0:
		best = max(best, stock[-1])
		return stock[-1]

	if stock[-1] + ((time_left-1)**2 + (time_left-1)) // 2  + time_left * robots[-1] < best:
		return -1

	if next_bot_type < 0:
		result = max(dfs(state, cache, blp, upper, idx) for idx, _ in enumerate(blp))
		cache[state] = result
		return result

	if next_bot_type < 3:
		enough_of_robot_type = robots[next_bot_type] >= upper[next_bot_type]
		enough_of_ressource = robots[next_bot_type] * time_left + stock[next_bot_type] >= time_left * upper[next_bot_type]
		if enough_of_robot_type or enough_of_ressource:
			return -1

	production = tuple(n + bot for n, bot in zip(stock, robots))

	if any(cost > n for cost, n in zip(blp[next_bot_type], stock)):
		new_state = (time_left-1, production, robots)
		return dfs(new_state, cache, blp, upper, next_bot_type)

	new_stock = tuple(n - cost for n, cost in zip(production, blp[next_bot_type]))
	new_robots = tuple(bot + (next_bot_type==idx) for idx, bot in enumerate(robots))
	new_state = (time_left-1, new_stock, new_robots)
	return dfs(new_state, cache, blp, upper, -1)


with open("input.txt") as file:
	blocks = [re.findall(r"\d+", line) for line in file]

p1_acc, p2_acc = 0, 1
for idx, numbers in enumerate(blocks):
	blueprint = (
		(int(numbers[1]),0,0,0),
		(int(numbers[2]),0,0,0),
		(int(numbers[3]),int(numbers[4]),0,0),
		(int(numbers[5]),0,int(numbers[6]),0),
	)
	upper_bounds = tuple(max(b[i] for b in blueprint) for i in range(3))

	best = 0
	init_state = (24, (0,0,0,0), (1,0,0,0))
	p1_acc += dfs(init_state, {}, blueprint, upper_bounds, -1) * (idx + 1)
	init_state = (32, (0,0,0,0), (1,0,0,0))
	p2_acc *= dfs(init_state, {}, blueprint, upper_bounds, -1) if idx < 3 else 1

print(f"Part 1: {p1_acc}")
print(f"Part 2: {p2_acc}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
