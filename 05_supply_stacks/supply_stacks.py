import re
import string
import time

from collections import defaultdict

begin = time.time()

###

UPPERCASE_LETTERS = set(string.ascii_uppercase)

def parse_stacks(inp: str) -> list:
	d = defaultdict(list)
	for line in inp.split("\n"):
		for idx, char in enumerate(line):
			if char in UPPERCASE_LETTERS:
				d[idx].append(char)
	return [list(reversed(d[key])) for key in sorted(d.keys())]


with open("input.txt") as file:
	stack_input, move_input = file.read().strip().split("\n\n")

stacks_p1 = parse_stacks(stack_input)
stacks_p2 = parse_stacks(stack_input)
moves = [[int(number) for number in re.findall(r"\d+", line)] for line in move_input.split("\n")]

for n, source, target in moves:
	stacks_p1[target-1] += [stacks_p1[source-1].pop() for _ in range(n)]
	stacks_p2[target-1] += reversed([stacks_p2[source-1].pop() for _ in range(n)])

print(f"Part 1: {''.join(stack[-1] for stack in stacks_p1)}")
print(f"Part 2: {''.join(stack[-1] for stack in stacks_p2)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
