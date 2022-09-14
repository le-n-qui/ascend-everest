# import libraries
import glob
import math
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
		print(col, end=' ')
		if row - 1 >= 0 and col <= (len(seq_list[row-1]) - 1): # northern neighbor
			neighbors.append(seq_list[row-1][col])

		if row - 1 >= 0 and col - 1 >= 0 and col - 1 <= (len(seq_list[row-1]) - 1): # north west
			neighbors.append(seq_list[row-1][col-1])

		if row - 1 >= 0 and col + 1 <= (len(seq_list[row-1]) - 1): # north east
			neighbors.append(seq_list[row-1][col+1])

		if row + 1 < num_rows and col <= (len(seq_list[row+1]) - 1): # southern neighbor
			neighbors.append(seq_list[row+1][col])

		if row + 1 < num_rows and col - 1 >= 0 and col - 1 <= (len(seq_list[row+1]) - 1): # south west
			neighbors.append(seq_list[row+1][col-1])

		if row + 1 < num_rows and col + 1 <= (len(seq_list[row+1]) - 1): # south east
			neighbors.append(seq_list[row+1][col+1])

		if col - 1 >= 0: # western neighbor
			neighbors.append(seq_list[row][col-1])

		if col + 1 < num_cols: # eastern neighbor
			neighbors.append(seq_list[row][col+1])

		graph_map[seq_list[row][col]] = neighbors

	
	
# print the map using the saved list of lists
for seq in guide_map:
	print("".join(seq), end='')



def heuristic_function_0(explorer, summit):
	delta_x = explorer.get_x_pos() - summit.get_x_pos()
	delta_y = explorer.get_y_pos() - summit.get_y_pos()
	delta_z = explorer.get_x_pos() - summit.get_z_pos()

	return math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

def heuristic_function_1(explorer, summit):
	# Manhattan distance
	delta_x = explorer.get_x_pos() - summit.get_x_pos()
	delta_y = explorer.get_y_pos() - summit.get_y_pos()

	return math.sqrt(delta_x**2 + delta_y**2) 

def heuristic_function_2(explorer, summit):
	pass

def get_minimum(dict_unvisited_nodes):
	minimum_f_score = sys.max_size

	for node in dict_unvisited_nodes:
		if dict_unvisited_nodes[node][F_SCORE] < minimum_f_score:
			minimum_f_score = dict_unvisited_nodes[node][F_SCORE]

	return minimum_f_score

def a_star_search(graph, start_node, target_node):
	pass