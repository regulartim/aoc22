import re
import time

begin = time.time()

###

DIRECTIONS = [(1,0),(0,1),(-1,0),(0,-1)]
MAP = {".": set(), "#": set(), " ": set()}

x_limit, y_limit = 0, 0

def cubic_wrap(x, y, d):
	match x, y, d:
		case _, 1, 3:
			wraped_pos = (0, x+100, 0) if x < 101 else (x-100, y+200, 3)
		case 150, _, 0:
			wraped_pos = (101, 151-y, 2)
		case _, 50, 1:
			wraped_pos = (101, x-50, 2)
		case 100, _, 0:
			wraped_pos = (y+50, 51, 3) if y < 101 else (151, 151-y, 2)
		case _, 150, 1:
			wraped_pos = (51, x+100, 2)
		case 50, _, 0:
			wraped_pos = (y-100, 151, 3)
		case _, 200, 1:
			wraped_pos = (x+100, 0, 1)
		case 1, _, 2:
			wraped_pos = (50, 151-y, 0) if y < 151 else (y-100, 0, 1)
		case _, 101, 3:
			wraped_pos = (50, x+50, 0)
		case 51, _, 2:
			wraped_pos = (0, 151-y, 0) if y < 51 else (y-50, 100, 1)
		case _:
			raise ValueError
	return wraped_pos

def move(x, y, d, n, part2) -> tuple:
	if n == 0:
		return (x, y, d)
	dx, dy = DIRECTIONS[d]
	n_x, n_y = x+dx, y+dy
	if (n_x, n_y) in MAP["#"]:
		return (x, y, d)
	if (n_x, n_y) in MAP["."]:
		return move(n_x, n_y, d, n-1, part2)
	if not part2:
		lx, ly, ld = move(n_x%x_limit, n_y%y_limit, d, n, part2)
	else:
		wx, wy, wd = cubic_wrap(x, y, d)
		assert (wx, wy) not in MAP["."]
		assert (wx, wy) not in MAP["#"]
		lx, ly, ld = move(wx, wy, wd, n, part2)
	return (lx, ly, ld) if (lx, ly) in MAP["."] else (x, y, d)

def get_password(numbers, turns, part2):
	x_pos, y_pos, direction = move(1, 1, 0, 1, False)
	for number, turn in zip(numbers, turns):
		x_pos, y_pos, direction = move(x_pos, y_pos, direction, number, part2)
		direction = (direction + turn) % 4
	return 4*x_pos + 1000*y_pos + direction


with open("input.txt") as file:
	map_block, path_block = file.read().split("\n\n")

for y_idx, line in enumerate(map_block.split("\n")):
	for x_idx, char in enumerate(line):
		MAP[char].add((x_idx+1,y_idx+1))
		x_limit, y_limit = max((x_limit, x_idx+3)), max((y_limit, y_idx+3))

path_numbers = [int(n) for n in re.findall(r"\d+", path_block)]
path_turns = [-1 if char == "L" else 1 for char in re.findall(r"[A-Z]", path_block)] + [0]

print(f"Part 1: {get_password(path_numbers, path_turns, False)}")
print(f"Part 2: {get_password(path_numbers, path_turns, True)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
