import ast
import time

begin = time.time()

###

DIVIDER_PACKETS = [[[2]],[[6]]]

def is_ordered(left, right) -> int:
	match left, right:
		case int(), list():
			return is_ordered([left], right)
		case list(), int():
			return is_ordered(left, [right])
		case int(), int():
			return 1 if left < right else -1 if left > right else 0

	results = [is_ordered(*pair) for pair in zip(left, right)]
	stop_default = -1 if len(left) > len(right) else 1 if len(left) < len(right) else 0
	return next((result for result in results if result != 0), stop_default)


with open("input.txt") as file:
	packets = [ast.literal_eval(line.strip()) for line in file if line.strip()]

pairs = [(packets[i], packets[i+1]) for i in range(0, len(packets), 2)]
divider_indices = [sum(is_ordered(other, divider) == 1 for other in packets + DIVIDER_PACKETS) + 1
					for divider in DIVIDER_PACKETS]

print(f"Part 1: {sum(idx+1 for idx, pair in enumerate(pairs) if is_ordered(*pair) == 1)}")
print(f"Part 2: {divider_indices[0] * divider_indices[1]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
