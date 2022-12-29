import functools
import re
import time

from itertools import combinations

import networkx as nx

begin = time.time()

###

G = nx.Graph()
STARTING_POSITION = "AA"
P1_MINUTES, P2_MINUTES = 30, 26


@functools.cache
def dfs(position: str, minutes_left: int, valves_left: frozenset) -> int:
	best_result = 0
	for v in valves_left:
		time_delta = minutes_left - shortest_path_lengths[(position,v)]
		if time_delta < 1:
			continue
		release = flow_rates[v] * time_delta
		path_release = dfs(v, time_delta, valves_left - {v})
		result = path_release + release
		best_result = max([result, best_result])
	return best_result

def work_with_elefant(valves: frozenset) -> int:
	max_release = 0
	for my_valves in combinations(valves, len(valves) // 2):
		my_valves = frozenset(my_valves)
		my_release = dfs(STARTING_POSITION, P2_MINUTES, my_valves)
		if my_release < max_release // 2:
			continue
		ele_release = dfs(STARTING_POSITION, P2_MINUTES, valves - my_valves)
		max_release = max((max_release, my_release + ele_release))
	return max_release

with open("input.txt") as file:
	lines = [line.strip() for line in file]

flow_rates = {}
for line in lines:
	valve, *others = re.findall(r"[A-Z]{2}", line)
	G.add_edges_from((valve, other) for other in others)
	flow_rates[valve] = int(re.findall(r"\d+", line)[0])

working_valves = frozenset(v for v, rate in flow_rates.items() if rate > 0)

shortest_path_lengths = {}
for start, targets in nx.all_pairs_shortest_path(G):
	for target, path in targets.items():
		shortest_path_lengths[(start, target)] = len(path)

print(f"Part 1: {dfs(STARTING_POSITION, P1_MINUTES, working_valves)}")
print(f"Part 2: {work_with_elefant(working_valves)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
