import time

from collections import deque

begin = time.time()

###

def get_neighbors(x: int, y: int, z: int) -> tuple:
	return (
		(x-1,y,z),(x+1,y,z),
		(x,y-1,z),(x,y+1,z),
		(x,y,z-1),(x,y,z+1)
	)

def get_adjacent_air(cube: tuple, others: set) -> list:
	return [n for n in get_neighbors(*cube) if n not in others]

def count_ext_surface(start: tuple, lower_bound: int, upper_bound: int, cubes: set) -> int:
	q = deque([start])
	seen = {start}
	ext_surface_count = 0
	while q:
		adjacent_air = get_adjacent_air(q.pop(), cubes)
		ext_surface_count += 6 - len(adjacent_air)
		for cube in adjacent_air:
			if cube in seen or min(cube) < lower_bound or max(cube) > upper_bound:
				continue
			q.appendleft(cube)
			seen.add(cube)
	return ext_surface_count


with open("input.txt") as file:
	lines = {tuple(int(n) for n in line.strip().split(",")) for line in file}

min_value = min(min(dim for dim in cube) for cube in lines)
max_value = max(max(dim for dim in cube) for cube in lines)

leftmost_cube = min(lines)
outside_cube = (leftmost_cube[0]-1, *leftmost_cube[1:])

print(f"Part 1: {sum(len(get_adjacent_air(cube, lines)) for cube in lines)}")
print(f"Part 2: {count_ext_surface(outside_cube, min_value-1, max_value+1, lines)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
