import time
from collections import deque, namedtuple

begin = time.time()

###

DECRYPTION_KEY = 811589153

Number = namedtuple("Number", ["id", "value"])

def mix(lst: list, factor: int, n_times: int):
	size = len(lst)
	lst = [Number(id=number.id, value=number.value*factor) for number in lst]
	deq = deque(lst)
	for _ in range(n_times):
		for number in lst:
			deq.rotate(-deq.index(number))
			deq.popleft()
			deq.insert(number.value % (size-1), number)
	return deq

def get_coordinates(deq: list):
	while deq[0].value != 0:
		deq.rotate(-1)
	for _ in range(3):
		deq.rotate(-1000)
		yield deq[0].value


with open("input.txt") as file:
	encrypted_file = [Number(id=idx, value=int(line)) for idx, line in enumerate(file)]

print(f"Part 1: {sum(get_coordinates(mix(encrypted_file, 1, 1)))}")
print(f"Part 2: {sum(get_coordinates(mix(encrypted_file, DECRYPTION_KEY, 10)))}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
