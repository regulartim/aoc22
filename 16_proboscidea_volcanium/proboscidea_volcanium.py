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
	if minutes_left < 1:
		return 0

	release = flow_rates[position] * (minutes_left-1)
	minutes_left -= release > 0

	if not valves_left:
		return release

	posibilities = []
	for v in valves_left:
		distance = len(shortest_paths[position][v]) - 1
		posibilities.append(release + dfs(v, minutes_left - distance, valves_left - {v}))
	return max(posibilities)

def work_with_elefant(valves: frozenset) -> int:
	max_release = -1
	for my_valves in combinations(valves, len(valves)//2):
		my_valves = frozenset(my_valves)
		my_release = dfs(STARTING_POSITION, P2_MINUTES, my_valves)
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
shortest_paths = dict(nx.all_pairs_shortest_path(G))

print(f"Part 1: {dfs(STARTING_POSITION, P1_MINUTES, working_valves)}")
print(f"Part 2: {work_with_elefant(working_valves)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
