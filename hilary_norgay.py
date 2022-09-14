# import libraries
import glob
import heapq
import math
import sys

from Node import Node

# retrieve file name
test_file = sys.argv[1]

# retrieve heuristic function
# cast a text-based number into integer
heuristic = int(sys.argv[2]) 

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

	
	
def print_terrain_map():
	pass

# print the map using the saved list of lists
# for seq in guide_map:
# 	print("".join(seq), end='')

# Indices for c cost, 
# f cost, and previous node
C_SCORE = 0
F_SCORE = 1
PREVIOUS = 2


def heuristic_function_0(explorer, summit):
	delta_x = explorer.get_x_pos() - summit.get_x_pos()
	delta_y = explorer.get_y_pos() - summit.get_y_pos()
	delta_z = explorer.get_z_pos() - summit.get_z_pos()

	return math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

def heuristic_function_1(explorer, summit):
	# Manhattan distance
	delta_x = explorer.get_x_pos() - summit.get_x_pos()
	delta_y = explorer.get_y_pos() - summit.get_y_pos()

	return math.sqrt(delta_x**2 + delta_y**2) 

def heuristic_function_2(explorer, summit):
	pass

def get_heuristic(current_node, target_node):
	h_score_value = None

	if heuristic == 0:
		#print("Use heuristic ZERO")
		h_score_value = heuristic_function_0(current_node, target_node)
	elif heuristic == 1:
		#print("Use heuristic ONE")
		h_score_value = heuristic_function_1(current_node, target_node)
	else:
		#print("Use heuristic TWO")
		h_score_value = heuristic_function_2(current_node, target_node)

	return h_score_value

# Return the node with the lowest f score
# Implementation can be done with priority queue
def get_minimum(dict_unvisited_neighbors): # dict of neighboring nodes
	minimum_f_score = sys.maxsize
	node_lowest_fscore = None

	for node in dict_unvisited_neighbors:
		#node.print_node_info()
		#print(dict_unvisited_nodes[node][F_SCORE])
		if dict_unvisited_neighbors[node][F_SCORE] < minimum_f_score:
			minimum_f_score = dict_unvisited_neighbors[node][F_SCORE]
			node_lowest_fscore = node

	return node_lowest_fscore

# Search function with A* algorithm implementation
def a_star_search(graph, start_node, target_node):
	# Create lists for visited and unvisited nodes
	visited = {}
	unvisited = {}

	# Add and initialize every node to the unvisited list
	for node in graph_map:
		# each node has a list of c cost, f cost, and previous node
		# starting out with infinity, infinity, and None
		unvisited[node] = [sys.maxsize, sys.maxsize, None]

	# Update the values for the start node in the unvisited list 
	f_score_value = get_heuristic(start_node, target_node)

	unvisited[start_node] = [0, f_score_value, None]

	current_node = start_node

    # Loop until the unvisited list becomes empty
	done = False

	while not done:
    	# Verify if there are nodes in unvisited list
		if len(unvisited) == 0:
			done = True
		else:
    		# Create a local dict to store unvisited neighbor nodes	
			unvisited_neighbors = {} 
			
    		# Check if current node is the target node
			if current_node == target_node:
				done = True
				visited[current_node] = unvisited[current_node]
			else:
    			# Get the list of current node's neighbors
				neighbors = graph_map[current_node]

    			# Loop through each node in neighbors list
				for neighbor in neighbors:
    				# Check if the neighbor node has already been visited
					if neighbor not in visited:
    					# Calculate new c score
						new_c_score = unvisited[current_node][C_SCORE] + 1

						if new_c_score < unvisited[neighbor][C_SCORE]:
    						# Update c, f, and previous node for neighbor
							unvisited[neighbor][C_SCORE] = new_c_score
							unvisited[neighbor][F_SCORE] = new_c_score + get_heuristic(neighbor, target_node)
							unvisited[neighbor][PREVIOUS] = current_node
							# save all unvistied neighbors in this local dict copy
							unvisited_neighbors[neighbor] = unvisited[neighbor] 

    			# Add current node to the visited list
				visited[current_node] = unvisited[current_node]

    			# Remove current node from the unvisited list
				del unvisited[current_node]

				# Get the unvisited node with the lowest f score value
				current_node = get_minimum(unvisited_neighbors) 

    # TODO: return the final visited list
	return visited


# Test
result_map = a_star_search(graph_map, explorer_node, summit_node)
for node in result_map:
	node.print_node_info()
    

   
	