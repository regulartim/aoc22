import re 
import time

begin = time.time()

###

P1_Y_IDX = 2_000_000

def manhattan_dist(xa :int, ya: int, xb: int, yb: int) -> int:
	return abs(xa - xb) + abs (ya - yb)

def get_row_coverage(sensor: list, distance: int, row: int) -> tuple:
	x, y = sensor
	radius_at_row = distance - abs(row - y)
	if radius_at_row < 0:
		return None
	return x - radius_at_row, x + radius_at_row

def count_covered_postions(row_coverages: list) -> int:
	current = row_coverages[0][0]
	acc = 0
	gaps = []
	for start, stop in row_coverages:
		if current < start:
			gaps.append(current)
		if current > stop:
			continue
		acc += 1 + stop - max(start, current)
		current = stop + 1
	return acc, gaps

def get_row_properties(report: list, distances: list) -> list:
	result = []
	for y in range(P1_Y_IDX*2):
		row_coverages = [get_row_coverage(line[:2], distance, y) for line, distance in zip(report, distances)]
		row_coverages = sorted([c for c in row_coverages if c])
		covered_positions, gaps = count_covered_postions(row_coverages)
		beacons_in_row = set(line[2] for line in report if line[3] == y)
		result.append((covered_positions - len(beacons_in_row), gaps))
	return result


with open("input.txt") as file:
	sensors_report = [[int(n) for n in re.findall(r"-?\d+", line)] for line in file]

beacon_distances = [manhattan_dist(*line) for line in sensors_report]
row_properties = get_row_properties(sensors_report, beacon_distances)
distress_x, distress_y = next((row[1][0], y) for y, row in enumerate(row_properties) if row[1])

print(f"Part 1: {row_properties[P1_Y_IDX][0]}")
print(f"Part 2: {distress_x * 4000000 + distress_y}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
