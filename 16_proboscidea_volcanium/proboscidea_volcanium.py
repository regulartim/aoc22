import re 
import time

from itertools import combinations

import networkx as nx

begin = time.time()

###

G = nx.Graph()
STARTING_POSITION = "AA"
P1_MINUTES, P2_MINUTES = 30, 26


def dfs(position, minutes_left, valves_left):
	if minutes_left < 1:
		return 0

	release = flow_rates[position] * (minutes_left-1)
	minutes_left -= release > 0

	if not valves_left:
		return release

	posibilities = []
	for next_valve in valves_left:
		distance = len(shortest_paths[position][next_valve]) - 1
		posibilities.append(release + dfs(next_valve, minutes_left - distance, valves_left - {next_valve}))
	return max(posibilities)


with open("input.txt") as file:
	lines = [line.strip() for line in file]

flow_rates = {}
for line in lines:
	valve, *others = re.findall(r"[A-Z]{2}", line)
	G.add_edges_from((valve, other) for other in others)
	flow_rates[valve] = int(re.findall(r"\d+", line)[0])

working_valves = {v for v, rate in flow_rates.items() if rate > 0}
shortest_paths =  dict(nx.all_pairs_shortest_path(G))

p2_result = 0
for my_valves in combinations(working_valves, len(working_valves)//2):
	my_valves = set(my_valves)
	elefants_valves = working_valves - my_valves
	flow_ratio = sum(flow_rates[v] for v in my_valves) / sum(flow_rates[v] for v in elefants_valves)
	if not 0.75 < flow_ratio < 1.5:
		continue
	my_release = dfs(STARTING_POSITION, P2_MINUTES, my_valves)
	elefants_release = dfs(STARTING_POSITION, P2_MINUTES, elefants_valves)
	p2_result = max((p2_result, my_release + elefants_release))

print(f"Part 1: {dfs(STARTING_POSITION, P1_MINUTES, working_valves)}")
print(f"Part 2: {p2_result}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
