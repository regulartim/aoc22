import heapq
import time

from functools import cache

begin = time.time()

###

NEIGHBOURHOOD = ((0,0),(0,1),(1,0),(-1,0),(0,-1))


def manhattan_dist(a: tuple, b: tuple) -> int:
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

@cache
def blizzards_at(minute: int) -> frozenset:
	max_x, max_y = GOAL[0]+1, GOAL[1]
	return frozenset(((x + dx*minute) % max_x, (y + dy*minute) % max_y) for x, y, dx, dy in BLIZZARDS)

def get_neighbours(point: tuple, minute: int):
	coming_blizzards = blizzards_at(minute + 1)
	for delta in NEIGHBOURHOOD:
		neighbour = (point[0] + delta[0], point[1] + delta[1])
		if neighbour not in GROUND:
			continue
		if neighbour in coming_blizzards:
			continue
		yield neighbour

def a_star(start: tuple, at_minute: int, target: tuple) -> int:
	q = [(manhattan_dist(start, target), at_minute, start)]
	heapq.heapify(q)
	seen = {(start, at_minute)}
	while q:
		_, minute, point = heapq.heappop(q)
		if point == target:
			return minute
		for neighbour in get_neighbours(point, minute):
			if (neighbour, minute+1) in seen:
				continue
			seen.add((neighbour, minute+1))
			heapq.heappush(q, (minute+1 + manhattan_dist(neighbour, target), minute+1, neighbour))


with open("input.txt") as file:
		lines = [line.strip() for line in file]

ground, blizzards = [], []
for y_idx, line in enumerate(lines):
	for x_idx, char in enumerate(line):
		match char:
			case ".":
				pass
			case ">":
				blizzards.append((x_idx-1, y_idx-1, 1, 0))
			case "<":
				blizzards.append((x_idx-1, y_idx-1, -1, 0))
			case "v":
				blizzards.append((x_idx-1, y_idx-1, 0, 1))
			case "^":
				blizzards.append((x_idx-1, y_idx-1, 0, -1))
			case _:
				continue
		ground.append((x_idx-1, y_idx-1))

GROUND, BLIZZARDS = frozenset(ground), frozenset(blizzards)
START, GOAL = min(ground), max(ground)

start_to_goal = a_star(START, 0, GOAL)
back_to_start = a_star(GOAL, start_to_goal, START)
back_to_goal = a_star(START, back_to_start, GOAL)

print(f"Part 1: {start_to_goal}")
print(f"Part 2: {back_to_goal}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
