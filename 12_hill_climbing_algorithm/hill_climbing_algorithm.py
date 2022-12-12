import string
import time
import heapq

import numpy as np

begin = time.time()

###

HEIGHT = {char: idx for idx, char in enumerate(string.ascii_lowercase)}
HEIGHT["S"] = 0
HEIGHT["E"] = 25


def get_neighbors(point: tuple, grid: list, part2: bool):
	for diff in [(0,1), (1,0), (-1,0), (0,-1)]:
		x, y = point[0] + diff[0], point[1] + diff[1]
		x_limit, y_limit = grid.shape
		if not -1 < x < x_limit or not -1 < y < y_limit:
			continue
		if not part2 and HEIGHT[grid[x,y]] > HEIGHT[grid[point]] + 1:
			continue
		if part2 and HEIGHT[grid[x,y]] < HEIGHT[grid[point]] - 1:
			continue
		yield x, y

def get_shortest_path(grid: list, start: tuple, target: str, part2: bool):
	queue = [(0, start)]
	heapq.heapify(queue)
	seen = {start}
	while queue:
		cost, current = heapq.heappop(queue)
		if grid[current] == target:
			return cost
		for neighbor in get_neighbors(current, grid, part2):
			if neighbor in seen:
				continue
			seen.add(neighbor)
			heapq.heappush(queue, (cost + 1, neighbor))
	return -1


with open("input.txt") as file:
	heightmap = np.array([list(line.strip()) for line in file])

start_idx = tuple(arr[0] for arr in np.where(heightmap=="S"))
end_idx = tuple(arr[0] for arr in np.where(heightmap=="E"))

print(f"Part 1: {get_shortest_path(heightmap, start_idx, 'E', False)}")
print(f"Part 2: {get_shortest_path(heightmap, end_idx, 'a', True)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
