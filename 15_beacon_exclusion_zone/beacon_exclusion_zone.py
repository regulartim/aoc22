import re 
import time

begin = time.time()

###

P1_Y_IDX = 2_000_000

def manhattan_dist(xa :int, ya: int, xb: int, yb: int) -> int:
	return abs(xa - xb) + abs (ya - yb)

def get_row_coverage(sensor: tuple, distance: int, row: int) -> tuple:
	x, y = sensor
	radius_at_row = distance - abs(row - y)
	if radius_at_row < 0:
		return None
	return x - radius_at_row, x + radius_at_row

def merge_intervals(intervals: list) -> tuple:
	intervals.sort()
	result = intervals[0]
	for start, stop in intervals[1:]:
		if result[1] + 1 < start:
			break
		result = result[0], max(result[1], stop)
	return result

def get_coverage_interval(report: list, distances: list, y: int) -> tuple:
	row_coverages = [get_row_coverage(line[:2], dist, y) for line, dist in zip(report, distances)]
	return merge_intervals([i for i in row_coverages if i])

def find_interval_gap(report: list, distances: list) -> tuple:
	for y in range(P1_Y_IDX * 2):
		coverage_interval = get_coverage_interval(report, distances, y)
		if coverage_interval[1] < P1_Y_IDX * 2:
			return coverage_interval[1] + 1, y


with open("input.txt") as file:
	sensors_report = [tuple(int(n) for n in re.findall(r"-?\d+", line)) for line in file]
beacon_distances = [manhattan_dist(*line) for line in sensors_report]

coverage_start, coverage_stop = get_coverage_interval(sensors_report, beacon_distances, P1_Y_IDX)
beacons_in_row = set(line[2] for line in sensors_report if line[3] == P1_Y_IDX)
blocked_postions = abs(coverage_start - coverage_stop) + 1 - len(beacons_in_row)

gap_x, gap_y = find_interval_gap(sensors_report, beacon_distances)

print(f"Part 1: {blocked_postions}")
print(f"Part 2: {gap_x * 4000000 + gap_y}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
