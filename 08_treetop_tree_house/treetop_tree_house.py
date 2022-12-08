import time

import numpy as np

begin = time.time()

###

def viewing_distance(tree: int, trees_in_line: list) -> int:
	viewing_dist = 0
	for other in trees_in_line:
		viewing_dist += 1
		if other >= tree:
			break
	return viewing_dist

def update_visibles(visibles: list, grid: list) -> list:
	for x, line in enumerate(grid):
		highest = -1
		for y, value in enumerate(line):
			if value > highest:
				highest = value
				visibles[x,y] = 1
	return visibles

def update_scores(scores: list, grid: list) -> list:
	for x, y in np.ndindex(grid.shape):
		scores[x,y] *= viewing_distance(grid[x,y], grid[x,y+1:])
	return scores


with open("input.txt") as file:
	tree_grid = np.array([list(line.strip()) for line in file.readlines()], dtype=int)

visible_trees = np.zeros(tree_grid.shape, int)
scenic_scores = np.ones(tree_grid.shape, int)

for _ in range(4):
	tree_grid = np.rot90(tree_grid)
	visible_trees = update_visibles(np.rot90(visible_trees), tree_grid)
	scenic_scores = update_scores(np.rot90(scenic_scores), tree_grid)

print(f"Part 1: {visible_trees.sum()}")
print(f"Part 2: {scenic_scores.max()}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
