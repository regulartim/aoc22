import string
import time

import numpy as np

begin = time.time()

###

def find_shared_item(rucksack: str) -> str:
	split_idx = len(rucksack)//2
	comp1, comp2 = set(rucksack[:split_idx]), set(rucksack[split_idx:])
	return comp1.intersection(comp2).pop()

def find_badge(group: list) -> str:
	a,b,c = [set(g) for g in group]
	return a.intersection(b).intersection(c).pop()

def get_priority(item: str):
	items = list(string.ascii_lowercase) + list(string.ascii_uppercase)
	return items.index(item) + 1


with open("input.txt") as file:
	rucksacks = [line.strip() for line in file.readlines()]

shared_items = [find_shared_item(rucksack) for rucksack in rucksacks]
elve_groups = np.reshape(rucksacks, (-1, 3))
badges = [find_badge(group) for group in elve_groups]

print(f"Part 1: {sum(get_priority(item) for item in shared_items)}")
print(f"Part 2: {sum(get_priority(badge) for badge in badges)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
