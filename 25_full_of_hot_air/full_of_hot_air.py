import time

begin = time.time()

###

SNAFU_DIGITS = {
	"=": -2,
	"-": -1,
	"0": 0,
	"1": 1,
	"2": 2
}


def snafu_add(a: list, b: list, carry=0) -> list:
	if not a and not b:
		return [carry] if carry else []

	if not a:
		return snafu_add([carry], b)

	if not b:
		return snafu_add(a, [carry])

	digit_sum = a[0] + b[0] + carry
	carry = int(digit_sum > 2) - int(digit_sum < -2)
	return [digit_sum - 5*carry] + snafu_add(a[1:], b[1:], carry)

def snafu_sum(numbers: list) -> str:
	acc = [0]
	for snafu in numbers:
		acc = snafu_add(acc, [SNAFU_DIGITS[char] for char in reversed(snafu)])
	return "".join(str(n) for n in reversed(acc)).replace("-1", "-").replace("-2", "=")


with open("input.txt") as file:
	snafu_numbers = [line.strip() for line in file]

print(f"Part 1: {snafu_sum(snafu_numbers)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
