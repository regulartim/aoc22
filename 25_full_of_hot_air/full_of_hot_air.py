import time

begin = time.time()

###

def snafu_to_int(snafu_number: str):
	acc = 0
	for idx, digit in enumerate(reversed(snafu_number)):
		match digit:
			case "=":
				value = -2
			case "-":
				value = -1
			case _:
				value = int(digit)
		acc += value * 5**idx
	return acc

def base_ten_to_base_five(n: int) -> str:
	base_five = ""
	while n > 0:
		remainder = n % 5
		base_five = str(remainder) + base_five
		n = n // 5
	return base_five

def int_to_snafu(n: int):
	result = []
	carry = 0
	for digit in reversed((base_ten_to_base_five(n))):
		digit = int(digit) + carry
		carry = int(digit > 2)
		result.append(digit - 5*carry)
	return "".join(str(n) for n in reversed(result)).replace("-1", "-").replace("-2", "=")


with open("input.txt") as file:
	snafu_numbers = [line.strip() for line in file]

as_int = [snafu_to_int(snafu) for snafu in snafu_numbers]

print(f"Part 1: {int_to_snafu(sum(as_int))}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
