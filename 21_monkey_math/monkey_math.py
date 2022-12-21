import time

begin = time.time()

###

OPERATIONS = {
	"+": lambda a, b: a + b,
	"-": lambda a, b: a - b,
	"*": lambda a, b: a * b,
	"/": lambda a, b: a // b,
}

class Node:
	def __init__(self, name: str):
		self.name = name
		self.value = -1
		self.children = []
		self.operation = None

	def evaluate(self) -> int:
		if self.value > 0:
			return self.value
		return OPERATIONS[self.operation](self.children[0].evaluate(), self.children[1].evaluate())

	def balance(self) -> int:
		left_result = self.children[0].evaluate()
		right_result = self.children[1].evaluate()
		self.children[0].expect(right_result)
		self.children[1].expect(left_result)

	def expect(self, result: int):
		if self.name == "humn":
			self.value = result
			return
		if self.value > 0:
			return
		match self.operation:
			case "+":
				# result = c0 + c1 => c0 = result - c1
				self.children[0].expect(result - self.children[1].evaluate())
				self.children[1].expect(result - self.children[0].evaluate())
			case "-":
				# result = c0 - c1 => c0 = result + c1 => c1 = c0 - result
				self.children[0].expect(result + self.children[1].evaluate())
				self.children[1].expect(self.children[0].evaluate() - result)
			case "*":
				# result = c0 * c1 => c0 = result // c1 => c1 = result // c0
				self.children[0].expect(result // self.children[1].evaluate())
				self.children[1].expect(result // self.children[0].evaluate())
			case "/":
				# result = c0 / c1 => c0 = result * c1 => c1 = c0 // result
				self.children[0].expect(result * self.children[1].evaluate())
				self.children[1].expect(self.children[0].evaluate() // result)


with open("input.txt") as file:
	inp = [line.split() for line in file]

monkeys = {line[0].strip(":"): Node(line[0].strip(":")) for line in inp}
for m, line in zip(monkeys.values(), inp):
	if len(line) < 4:
		m.value = int(line[-1])
		continue
	m.children = [monkeys[line[1]], monkeys[line[3]]]
	m.operation = line[2]

print(f"Part 1: {monkeys['root'].evaluate()}")
monkeys["root"].balance()
print(f"Part 2: {monkeys['humn'].value}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
