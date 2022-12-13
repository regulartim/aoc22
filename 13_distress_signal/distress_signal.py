import ast
import time

begin = time.time()

###

DIVIDER_PACKETS = [[[2]],[[6]]]

def compare(left, right) -> int:
	match left, right:
		case int(), list():
			return compare([left], right)
		case list(), int():
			return compare(left, [right])
		case int(), int():
			return left - right
		case list(), list():
			child_results = (compare(*pair) for pair in zip(left, right))
			stop_default = len(left) - len(right)
			return next((res for res in child_results if res != 0), stop_default)


with open("input.txt") as file:
	packets = [ast.literal_eval(line.strip()) for line in file if line.strip()]

pairs = [(packets[i], packets[i+1]) for i in range(0, len(packets), 2)]
divider_indices = [sum(compare(other, divider) < 0 for other in packets + DIVIDER_PACKETS) + 1
					for divider in DIVIDER_PACKETS]

print(f"Part 1: {sum(idx+1 for idx, pair in enumerate(pairs) if compare(*pair) < 0)}")
print(f"Part 2: {divider_indices[0] * divider_indices[1]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
