import time

from collections import deque

begin = time.time()

###

N1, N2 = 2022, 1000000000000
SAMPLE_SIZE = 4000
SHAPES = deque([
	((0,0),(1,0),(2,0),(3,0)),
	((1,0),(0,1),(1,1),(2,1),(1,2)),
	((0,0),(1,0),(2,0),(2,1),(2,2)),
	((0,0),(0,1),(0,2),(0,3)),
	((0,0),(1,0),(0,1),(1,1))
])


def get_resting_position(shape: tuple, resting: set, pattern: list, height: int) -> tuple:
	shape = ((x+2, y+height+4) for x, y in shape)
	while True:
		next_pos = tuple((x+pattern[0], y) for x, y in shape)
		if min(next_pos)[0] >= 0 and max(next_pos)[0] < 7 and resting.isdisjoint(next_pos):
			shape = next_pos
		pattern.rotate(-1)
		next_pos = tuple((x, y-1) for x, y in shape)
		if resting.isdisjoint(next_pos):
			shape = next_pos
			continue
		return shape, max((height, shape[-1][-1]))

def find_sequnece(lst: list) -> list:
	list_length = len(lst)
	for l in range(list_length // 2, 1, -1):
		if lst[list_length-2*l:list_length-l] == lst[list_length-l:]:
			return lst[list_length-l:]
	return []


with open("input.txt") as file:
	jet_pattern = deque(1 if char == ">" else -1 for char in file.read().strip())

resting_rock = {(x,0) for x in range(7)}

heights = [0]
for i in range(SAMPLE_SIZE):
	resting_shape, max_height = get_resting_position(SHAPES[0], resting_rock, jet_pattern, heights[-1])
	resting_rock.update(resting_shape)
	heights.append(max_height)
	SHAPES.rotate(-1)

sequence = find_sequnece([after-before for before, after in zip(heights, heights[1:])])
factor, rest = (N2-SAMPLE_SIZE) // len(sequence), (N2-SAMPLE_SIZE) % len(sequence)

print(f"Part 1: {heights[N1]}")
print(f"Part 2: {heights[-1] + factor * sum(sequence) + sum(sequence[:rest])}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
