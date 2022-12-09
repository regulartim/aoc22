import time

begin = time.time()

###

DIRECTIONS = {"U": (0,1), "D": (0,-1), "R": (1,0), "L": (-1,0)}

def move_point(point: tuple, direction: str) -> tuple:
	return point[0] + DIRECTIONS[direction][0], point[1] + DIRECTIONS[direction][1]

def follow_predecessor(point: tuple, predecessor: tuple) -> tuple:
	x_diff, y_diff = point[0] - predecessor[0], point[1] - predecessor[1]
	manhattan_distance = abs(x_diff) + abs(y_diff)
	is_diagonal_neighbour = abs(x_diff * y_diff) == 1

	if manhattan_distance < 2 or is_diagonal_neighbour:
		return point
	if abs(x_diff) > 0:
		point = move_point(point, "R" if x_diff < 0 else "L")
	if abs(y_diff) > 0:
		point = move_point(point, "U" if y_diff < 0 else "D")
	return point

def get_visited_postions(knot_count: int) -> set:
	visited = set()
	knots = [(0,0) for _ in range(knot_count)]
	for direction, step_count in motions:
		for _ in range(int(step_count)):
			knots[0] = move_point(knots[0], direction)
			for idx in range(1, knot_count):
				knots[idx] = follow_predecessor(knots[idx], knots[idx-1])
			visited.add(knots[-1])
	return visited


with open("input.txt") as file:
	motions = [line.split() for line in file.readlines()]

print(f"Part 1: {len(get_visited_postions(2))}")
print(f"Part 2: {len(get_visited_postions(10))}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
