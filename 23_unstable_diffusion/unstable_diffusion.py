import time

from collections import Counter

begin = time.time()

###

DIRECTIONS = [
	((0,-1),(1,-1),(-1,-1)),
	((0,1),(1,1),(-1,1)),
	((-1,0),(-1,-1),(-1,1)),
	((1,0),(1,-1),(1,1))
]

class Elf:
	proposal_counter = Counter()

	def __init__(self, position):
		self.position = position
		self.proposal = None

	def propose(self, grove, round_nr) -> tuple:
		options = []
		for main_dir in DIRECTIONS:
			adj = [(self.position[0] + dx, self.position[1] + dy) for dx, dy in main_dir]
			if any(pos in grove for pos in adj):
				options.append(None)
				continue
			options.append(adj[0])
		if all(o for o in options) or not any(o for o in options):
			self.proposal = None
			return None
		for idx in range(4):
			if options[(round_nr + idx) % 4]:
				self.proposal = options[(round_nr + idx) % 4]
				break
		self.proposal_counter[self.proposal] += 1
		return self.proposal

	def move(self):
		if self.proposal and self.proposal_counter[self.proposal] == 1:
			self.position = self.proposal
			self.proposal = None
		return self.position

def count_empty_tiles(grove):
	min_x, max_x = min(p[0] for p in grove), max(p[0] for p in grove)
	min_y, max_y = min(p[1] for p in grove), max(p[1] for p in grove)
	return (max_x-min_x+1) * (max_y-min_y+1) - len(grove)

def simulate(elves):
	grove = {e.position for e in elves}
	round_nr, part1_result, proposals = 0, 0, [True]
	while any(proposals):
		if round_nr == 10:
			part1_result = count_empty_tiles(grove)
		Elf.proposal_counter = Counter()
		proposals = [e.propose(grove, round_nr) for e in elves]
		grove = {e.move() for e in elves}
		round_nr += 1
	return part1_result, round_nr

with open("input.txt") as file:
	lines = [line.strip() for line in file]

elf_list = []
for y_idx, line in enumerate(lines):
	for x_idx, char in enumerate(line):
		if char == "#":
			elf_list.append(Elf((x_idx, y_idx)))

simualtion_result = simulate(elf_list)

print(f"Part 1: {simualtion_result[0]}")
print(f"Part 2: {simualtion_result[1]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
