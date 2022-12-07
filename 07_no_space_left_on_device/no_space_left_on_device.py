import time

begin = time.time()

###

THRESHOLD = 100000
TOTAL_DISK_SPACE = 70000000
REQUIRED_FREE_SPACE = 30000000

class Directory:

	def __init__(self, parent):
		self.parent = parent
		self.files = {}
		self.subdirs = {}
		self._size = -1

	def get_size(self) -> int:
		if self._size < 0:
			self._size = sum(self.files.values()) + sum(subdir.get_size() for subdir in self.subdirs.values())
		return self._size

	def get_subdir_sizes(self) -> list:
		result = [subdir.get_size() for subdir in self.subdirs.values()]
		for subdir in self.subdirs.values():
			result += subdir.get_subdir_sizes()
		return result


with open("input.txt") as file:
	terminal_output = [line.strip() for line in file.readlines()]

working_dir = None
root_dir = Directory(None)

for line in terminal_output:
	match line.split():
		case "$", "cd", "/":
			working_dir = root_dir
		case "$", "cd", "..":
			working_dir = working_dir.parent
		case "$", "cd", dir_name:
			working_dir = working_dir.subdirs[dir_name]
		case "$", "ls":
			pass
		case "dir", dir_name:
			working_dir.subdirs[dir_name] = Directory(working_dir)
		case size, file_name:
			working_dir.files[file_name] = int(size)

dir_sizes = [root_dir.get_size()] + root_dir.get_subdir_sizes()
unused_space = TOTAL_DISK_SPACE - root_dir.get_size()
space_to_free_up = REQUIRED_FREE_SPACE - unused_space

print(f"Part 1: {sum(size for size in dir_sizes if size < THRESHOLD)}")
print(f"Part 2: {min(size for size in dir_sizes if size > space_to_free_up)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
