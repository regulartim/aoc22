import re
import time

from functools import cache

begin = time.time()

###

@cache
def heuristic(time_left: int, geode_robot_count: int) -> int:
	return ((time_left-1)**2 + (time_left-1)) // 2  + time_left * geode_robot_count

@cache
def dfs(time_left: int, stock: tuple, robots: tuple, blueprint: tuple, upper: tuple) -> int:
	global best

	if time_left == 0:
		return stock[-1]

	if stock[-1] + heuristic(time_left, robots[-1]) < best:
		return -1

	production = tuple(n + bot for n, bot in zip(stock, robots))

	save = False
	child_results = []
	for idx, costs in enumerate(blueprint):
		if idx < 3 and robots[idx] >= upper[idx]:
			continue
		if idx < 3 and robots[idx] * time_left + stock[idx] >= time_left * upper[idx]:
			continue
		if any(cost > n for cost, n in zip(costs, stock)):
			save = True
			continue
		new_robots = tuple(bot + (idx==jdx) for jdx, bot in enumerate(robots))
		new_stock = tuple(n - cost for n, cost in zip(production, costs))
		child_results.append(dfs(time_left-1, new_stock, new_robots, blueprint, upper))

	if save:
		child_results.append(dfs(time_left-1, production, robots, blueprint, upper))

	result = max(child_results)
	best = max(best, result)
	return result


with open("input.txt") as file:
	blocks = [re.findall(r"\d+", line) for line in file]

blueprints, upper_bounds = [], []
for numbers in blocks:
	blp = (
		(int(numbers[1]),0,0,0),
		(int(numbers[2]),0,0,0),
		(int(numbers[3]),int(numbers[4]),0,0),
		(int(numbers[5]),0,int(numbers[6]),0),
	)
	blueprints.append(blp)
	upper_bounds.append(tuple(max(b[i] for b in blp) for i in range(3)))

best = 0
quality_levels = []
for i, tup in enumerate(zip(blueprints, upper_bounds)):
	open_geodes = dfs(24, (0,0,0,0), (1,0,0,0), *tup)
	quality_levels.append(open_geodes * (i + 1))
	dfs.cache_clear()
	best = 0

print(f"Part 1: {sum(quality_levels)}")

acc = 1
for tup in zip(blueprints[:3], upper_bounds):
	acc *= dfs(32, (0,0,0,0), (1,0,0,0), *tup)
	dfs.cache_clear()
	best = 0

print(f"Part 2: {acc}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
