import time

import networkx as nx

begin = time.time()

###

def get_neighbors(x: int, y: int, z: int) -> tuple:
	return (
		(x-1,y,z),(x+1,y,z),
		(x,y-1,z),(x,y+1,z),
		(x,y,z-1),(x,y,z+1)
	)

def build_graph(cubes: set):
	G = nx.Graph()
	for cube in cubes:
		for air in get_surface(cube, cubes):
			G.add_edges_from((air, other) for other in get_surface(air, cubes))
	return G

def get_surface(cube: tuple, others: set) -> list:
	return [n for n in get_neighbors(*cube) if n not in others]

def count_outside_facing_sides(outside_point: tuple, cubes: set, graph) -> int:
	acc = 0
	for cube in cubes:
		for air in get_surface(cube, cubes):
			if air not in graph:
				continue
			acc += nx.has_path(graph, outside_point, air)
	return acc


with open("input.txt") as file:
	lines = {tuple(int(n) for n in line.strip().split(",")) for line in file}

leftmost_cube = min(lines)
outside = (leftmost_cube[0]-1, *leftmost_cube[1:])
air_graph = build_graph(lines)

print(f"Part 1: {sum(len(get_surface(cube, lines)) for cube in lines)}")
print(f"Part 2: {count_outside_facing_sides(outside, lines, air_graph)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
