import re 
import time

import z3

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

def find_distress_beacon(report: list, distances: list) -> tuple:
	x = z3.Int("x")
	y = z3.Int("y")
	solver = z3.Solver()

	solver.add(0 < x, x < P1_Y_IDX * 2)
	solver.add(0 < y, y < P1_Y_IDX * 2)

	z3abs = lambda x: z3.If(x<0, -x, x)
	for r, dist in zip(report, distances):
		sx, sy, *_ = r
		solver.add(z3abs(sx-x) + z3abs(sy-y) > dist)
	solver.check()
	model = solver.model()
	return model[x].as_long(), model[y].as_long()


with open("input.txt") as file:
	sensors_report = [tuple(int(n) for n in re.findall(r"-?\d+", line)) for line in file]
beacon_distances = [manhattan_dist(*line) for line in sensors_report]

coverage_start, coverage_stop = get_coverage_interval(sensors_report, beacon_distances, P1_Y_IDX)
beacons_in_row = set(line[2] for line in sensors_report if line[3] == P1_Y_IDX)
blocked_postions = abs(coverage_start - coverage_stop) + 1 - len(beacons_in_row)

distress_x, distress_y = find_distress_beacon(sensors_report, beacon_distances)

print(f"Part 1: {blocked_postions}")
print(f"Part 2: {distress_x * 4000000 + distress_y}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
