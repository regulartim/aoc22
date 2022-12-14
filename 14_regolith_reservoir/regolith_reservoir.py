import time

begin = time.time()

###

SOURCE = (500,0)
VOID_DISTANCE = 10_000

def coordinates_between(point_a: str, point_b: str) -> set:
	xa, ya = (int(n) for n in point_a.split(","))
	xb, yb = (int(n) for n in point_b.split(","))
	result = {(xa, ya), (xb, yb)}

	match xa == xb, ya == yb:
		case True, False:
			for y in range(min(ya, yb), max(ya, yb)):
				result.add((xa, y))
		case False, True:
			for x in range(min(xa, xb), max(xa, xb)):
				result.add((x, ya))
	return result

def simulate_sand(solid_ground: set) -> tuple:
	position = SOURCE
	while position[1] < VOID_DISTANCE:
		for move_x, move_y in [(0,1),(-1,1),(1,1)]:
			new_pos = position[0] + move_x, position[1] + move_y
			if new_pos not in solid_ground:
				position = new_pos
				break
		else:
			return position
	return None

def count_resting_sand_units(solid_ground: set) -> int:
	rock_count = len(solid_ground)
	while True:
		resting_pos = simulate_sand(solid_ground)
		if not resting_pos:
			break
		solid_ground.add(resting_pos)
		if resting_pos == SOURCE:
			break
	return len(solid_ground) - rock_count


with open("input.txt") as file:
	lines = [line.strip().split(" -> ") for line in file]

rock = set()
for line in lines:
	for idx, p in enumerate(line[1:]):
		rock.update(coordinates_between(line[idx], p))

p1_rock = rock.copy()
max_y = max(point[1] for point in rock)
rock.update(coordinates_between(f"-{VOID_DISTANCE},{max_y+2}", f"{VOID_DISTANCE},{max_y+2}"))

print(f"Part 1: {count_resting_sand_units(p1_rock)}")
print(f"Part 2: {count_resting_sand_units(rock)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
