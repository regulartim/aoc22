import re
import time

import numpy as np

begin = time.time()

###

class Monkey:

	all_monkeys = []
	lcm_of_divisors = 0

	def __init__(self, block: list):
		self.seed = block
		self.items = [int(number) for number in re.findall(r"\d+", block[1])]
		match block[2].split()[-2:]:
			case "*", "old":
				self.operation = lambda old: old * old
			case "*", n:
				self.operation = lambda old: old * int(n)
			case "+", n:
				self.operation = lambda old: old + int(n)
		self.test_divisor = int(re.findall(r"\d+", block[3])[0])
		self.success_result = int(re.findall(r"\d+", block[4])[0])
		self.fail_result = int(re.findall(r"\d+", block[5])[0])
		self.inspection_count = 0

	def take_turn(self, part: int) -> None:
		for item in self.items:
			new = self.operation(item)
			worry_level = new // 3 if part == 1 else new % self.lcm_of_divisors
			target = self.success_result if worry_level % self.test_divisor == 0 else self.fail_result
			self.all_monkeys[target].items.append(worry_level)
		self.inspection_count += len(self.items)
		self.items = []


with open("input.txt") as file:
	blocks = [block.split("\n") for block in file.read().split("\n\n")]

solutions = []
for part in [1,2]:
	Monkey.all_monkeys = [Monkey(block) for block in blocks]
	Monkey.lcm_of_divisors = np.lcm.reduce([monkey.test_divisor for monkey in Monkey.all_monkeys])

	for _ in range(20 if part == 1 else 10_000):
		for monkey in Monkey.all_monkeys:
			monkey.take_turn(part)

	inspection_counts = sorted(monkey.inspection_count for monkey in Monkey.all_monkeys)
	solutions.append(inspection_counts[-1] * inspection_counts[-2])

print(f"Part 1: {solutions[0]}")
print(f"Part 2: {solutions[1]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
