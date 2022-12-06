import time

begin = time.time()

###

def find_marker(buffer: str, sequence_length: int) -> int:
	for idx in range(len(buffer)-sequence_length):
		sequence = buffer[idx:idx+sequence_length]
		if len(set(sequence)) < sequence_length:
			continue
		return idx+sequence_length


with open("input.txt") as file:
	datastream_buffer = file.read().strip()

print(f"Part 1: {find_marker(datastream_buffer, 4)}")
print(f"Part 2: {find_marker(datastream_buffer, 14)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
