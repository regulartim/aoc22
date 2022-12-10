import time

import numpy as np

begin = time.time()

###

CRT_WIDTH = 40
SIGNAL_INDIZES = [20, 60, 100, 140, 180, 220]

with open("input.txt") as file:
	program = [line.strip() for line in file.readlines()]

register = [1]
for instruction in program:
	register.append(register[-1])
	if instruction == "noop":
		continue
	_, value = instruction.split()
	register.append(register[-1] + int(value))

crt_content = "".join("#" if abs(cycle % CRT_WIDTH - sprite_pos) < 2 else " "
						for cycle, sprite_pos in enumerate(register[:-1]))
crt_lines = [crt_content[i:i+CRT_WIDTH] for i in range(0, len(crt_content), CRT_WIDTH)]

print(f"Part 1: {sum(i*register[i-1] for i in SIGNAL_INDIZES)}")
print(f"Part 2:\n{np.array(crt_lines)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
