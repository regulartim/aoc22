import time

begin = time.time()

###

def does_range_contain_other(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
	return a_start <= b_start <= b_end <= a_end \
		or b_start <= a_start <= a_end <= b_end

def do_ranges_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
	return a_start <= b_start <= a_end \
		or b_start <= a_start <= b_end


with open("input.txt") as file:
	lines = [line.strip().replace(",","-").split("-") for line in file.readlines()]
	section_pairs = [[int(n) for n in line] for line in lines]

print(f"Part 1: {sum(does_range_contain_other(*pair) for pair in section_pairs)}")
print(f"Part 2: {sum(do_ranges_overlap(*pair) for pair in section_pairs)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
