import heapq
import time

from functools import cache

begin = time.time()

###

NEIGHBOURHOOD = [(0,0),(0,1),(1,0),(-1,0),(0,-1)]

@cache
def manhattan_dist(a: tuple, b: tuple) -> int:
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

@cache
def blizzards_at(minute: int):
	goal = max(GROUND)
	x_limit, y_limit = goal[0]+1, goal[1]
	result = set()
	for x, y, dir_char in BLIZZARDS:
		match dir_char:
			case ">":
				dx, dy = minute, 0
			case "<":
				dx, dy = -minute, 0
			case "v":
				dx, dy = 0, minute
			case "^":
				dx, dy = 0, -minute
		new_pos = ((x+dx)%x_limit, (y+dy)%y_limit)
		result.add(new_pos)
	return frozenset(result)

@cache
def get_neighbours(point: tuple, minute) -> list:
	result = []
	coming_blizzards = blizzards_at(minute+1)
	for d in NEIGHBOURHOOD:
		neighbour = (point[0] + d[0], point[1] + d[1])
		if neighbour not in GROUND:
			continue
		if neighbour in coming_blizzards:
			continue
		result.append(neighbour)
	return result

def a_star(start: tuple, at_minute: int, target: tuple) -> int:
	q = [(manhattan_dist(start, target), at_minute, start)]
	heapq.heapify(q)
	seen = {(start, at_minute)}
	while q:
		_, dist, point = heapq.heappop(q)
		if point == target:
			return dist
		for neighbour in get_neighbours(point, dist):
			if (neighbour, dist+1) in seen:
				continue
			seen.add((neighbour, dist+1))
			heapq.heappush(q, (dist+1 + manhattan_dist(neighbour, target), dist+1, neighbour))


with open("input.txt") as file:
		lines = [line.strip() for line in file]

ground, blizzards = [], []
for y_idx, line in enumerate(lines):
	for x_idx, char in enumerate(line):
		if char == "#":
			continue
		if char != ".":
			blizzards.append((x_idx-1, y_idx-1, char))
		ground.append((x_idx-1, y_idx-1))

GROUND, BLIZZARDS = frozenset(ground), frozenset(blizzards)

start_to_target = a_star(min(ground), 0, max(ground))
back_to_start = a_star(max(ground), start_to_target, min(ground))
back_to_target = a_star(min(ground), back_to_start, max(ground))

print(f"Part 1: {start_to_target}")
print(f"Part 2: {back_to_target}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
