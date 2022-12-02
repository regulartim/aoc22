import time

begin = time.time()

###

SHAPES = ["A", "B", "C"]
P1_MAPPING = {
	"X": "A",
	"Y": "B",
	"Z": "C"
}


def get_score(a: str, b: str) -> int:
	b_index = SHAPES.index(b)
	shape_score = b_index + 1

	if a == SHAPES[(b_index-1) % 3]:
		return 6 + shape_score
	if a == b:
		return 3 + shape_score
	return shape_score

def choose_shape(a: str, round_result: str) -> str:
	a_index = SHAPES.index(a)

	match round_result:
		case "X": return SHAPES[(a_index-1) % 3]
		case "Y": return a
		case "Z": return SHAPES[(a_index+1) % 3]


with open("input.txt") as file:
	strategy = [line.split() for line in file.readlines()]

chosen_shapes = [(a, choose_shape(a, b)) for a, b in strategy]

print(f"Part 1: {sum(get_score(a, P1_MAPPING[b]) for a, b in strategy)}")
print(f"Part 2: {sum(get_score(a, b) for a, b in chosen_shapes)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
