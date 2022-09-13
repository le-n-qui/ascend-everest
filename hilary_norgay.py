# import libraries
import glob
import sys
from Node import Node

# retrieve file name
test_file = sys.argv[1]
# retrieve heuristic function
heuristic = sys.argv[2]

# a mapping 
elevation = {'~': 0, '.': 1, ':': 2, 'M': 3, 'S': 4}

# counter for x position on the map
x_counter = 0
# counter for y position on the map
y_counter = 0
# terrain map
guide_map = []
# node sequence list
seq_list = []
# terrain map represented as a graph
graph_map = {}
# starting position of the explorer
explorer_node = None # unknown for now
# position of the summit
summit_node = None # unknow for now

# store map content into a list of lists
with open(test_file) as file:
	# look at terrain map line by line
 	for line in file:
 		sequence = [] # a list of characters
 		node_list = [] # a list of nodes

 		# look at one line char by char
 		for char in line:
 			sequence.append(char)
 			if char == '\n': 
 				y_counter = 0
 				break
 			elif char.isnumeric():
 				explorer_node = Node(x_counter, y_counter, int(char))
 				node_list.append(explorer_node)
 			elif char == 'S':
 				summit_node = Node(x_counter, y_counter, elevation[char])
 				node_list.append(summit_node)

 			else:
 				node_list.append(Node(x_counter, y_counter, elevation[char]))
 			y_counter += 1

 		guide_map.append(sequence)
 		seq_list.append(node_list)
 		x_counter += 1


# create a graph represented by adjacency list of nodes
num_rows = len(seq_list)
for row in range(num_rows):
	num_cols = len(seq_list[row])
	for col in range(num_cols):
		neighbors = []
		if row - 1 >= 0 and col <= (len(seq_list[row-1]) - 1) : # northern neighbor
			neigbors.append(seq_list[row-1][col])

		if row - 1 >= 0 and col - 1 <= (len(seq_list[row-1]) - 1) : # north west
			# TODO
			pass

		if row + 1 < num_rows and col <= (len(seq_list[row+1]) - 1): # southern neighbor
			neigbors.append(seq_list[row+1][col])

		if col - 1 >= 0: # western neighbor
			# TODO
			pass

		if col + 1 < num_cols: # eastern neighbor
			# TODO
			pass


	print()

# print the map using the saved list of lists
for seq in guide_map:
	print("".join(seq), end='')

# Test
# print("\nTesting Area")
# explorer_node.print_node_info()
# summit_node.print_node_info()
# print("End testing")

