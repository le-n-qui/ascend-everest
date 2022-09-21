# import libraries
import glob
import heapq
import math
import sys
import time

from os import system
from Node import Node

# create clear function
# to refresh command line output
clear = lambda: system('clear')

# retrieve file name
test_file = sys.argv[1]

# retrieve heuristic function
# cast a text-based number into integer
heuristic = int(sys.argv[2]) 

# a mapping from character to number
elevation = {'~': 0, '.': 1, ':': 2, 'M': 3, 'S': 4}
# a mapping from number to character
codes = {0: '~', 1: '.', 2: ':', 3: 'M', 4: 'S'}

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
summit_node = None # unknown for now

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

	
# Function to display current terrain map
def print_terrain_map():
	# print the guide map 
	for seq in guide_map:
		print("".join(seq), end='')

# Function to trace from summit node
# to explorer node, and invoke
# map print function to generate
# the equence of maps
def trace_and_print(visited_nodes, explorer, summit):
	# Save the path of nodes 
	# into a stack
	stack = []
	# start the trace at summit node
	curr_node = summit
	# flag to stop loop
	finished = False

	while not finished:
		# examine previous node of current node
		previous_node = visited_nodes[curr_node][PREVIOUS]
		# is previous node the same as explorer node
		if previous_node == explorer:
			# push current node into stack first
			stack.append(curr_node)
			# then push previous node (explorer node) into stack
			stack.append(previous_node)
			# done with tracing
			finished = True
		else:
			# if previous node not the explorer node
			stack.append(curr_node)
			# go to that previous node
			curr_node = previous_node

	
	print('MAP PRINTING')
	print('------------')
	# pop the first node off the stack
	node = stack.pop() # explorer
	# start counter for map printing
	count = 0
	# print out the first map
	print('M_' + str(count))
	print_terrain_map()
	print('\n')

	# print subsequent maps
	while len(stack) != 0:
		# sleep for 2 seconds
		time.sleep(2)
		# clear command line screen 
		# for new map
		clear()
		# change popped node's elevation number into landscape symbol
		guide_map[node.get_x_pos()][node.get_y_pos()] = codes[node.get_z_pos()]
		# increment counter
		count += 1
		# examine next node in stack
		node = stack.pop()
		# change landscape symbol into elevation number 
		# i.e. explorer is now at this node
		guide_map[node.get_x_pos()][node.get_y_pos()] = str(node.get_z_pos())
		# print out the next map
		print('M_' + str(count))
		print_terrain_map()
		print('\n')

# Euclidean heuristic function
def heuristic_function_0(explorer, summit):
	delta_x = explorer.get_x_pos() - summit.get_x_pos()
	delta_y = explorer.get_y_pos() - summit.get_y_pos()
	delta_z = explorer.get_z_pos() - summit.get_z_pos()

	return math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

# Manhattan heuristic function
def heuristic_function_1(explorer, summit):
	delta_x = abs(explorer.get_x_pos() - summit.get_x_pos())
	delta_y = abs(explorer.get_y_pos() - summit.get_y_pos())

	return delta_x**2 + delta_y**2

# Diagonal heuristic function (uniform cost)
def heuristic_function_2(explorer, summit):
	cost = 1
	delta_x = abs(explorer.get_x_pos() - summit.get_x_pos())
	delta_y = abs(explorer.get_y_pos() - summit.get_y_pos())

	return cost * max(delta_x, delta_y)

# Retrieve the right heuristic function
# based on the given argument on the 
# command line terminal
def get_heuristic(current_node, target_node):
	h_score_value = None

	if heuristic == 0:
		# Use heuristic 0
		h_score_value = heuristic_function_0(current_node, target_node)
	elif heuristic == 1:
		# Use heuristic 1
		h_score_value = heuristic_function_1(current_node, target_node)
	else:
		# Otherwise, use heuristic 2
		h_score_value = heuristic_function_2(current_node, target_node)

	return h_score_value

# Indices for c cost, 
# f cost, and previous node
C_SCORE = 0
F_SCORE = 1
PREVIOUS = 2

# Search function with A* algorithm implementation
def a_star_search(graph, start_node, target_node):
	# Create lists for visited and unvisited nodes
	visited = {} # Format -- { Node: [c_score, f_score, previous_node] }
	unvisited = {} # Format -- { Node: [c_score, f_score, previous_node] }

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
    		# Create a local heap list
			unvisited_heap = []
			# Create a local dict to store 
			# unvisited neighboring nodes
			unvisited_neighbor_dict = {}
			
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

						# restrict which neighbor nodes the explorer can get to
						# by specifying the elevation difference to be 1
						if abs(current_node.get_z_pos() - neighbor.get_z_pos()) <= 1:
							
    						# Calculate new c score
							new_c_score = unvisited[current_node][C_SCORE] + 1

							if new_c_score < unvisited[neighbor][C_SCORE]:
								
    							# Update c, f, and previous node for neighbor
								unvisited[neighbor][C_SCORE] = new_c_score
								unvisited[neighbor][F_SCORE] = new_c_score + get_heuristic(neighbor, target_node)
								unvisited[neighbor][PREVIOUS] = current_node
						
							# store node into this local dict with key as id(node)
							unvisited_neighbor_dict[id(neighbor)] = neighbor
							# save tuple, e.g. (fscore, id(node)), in heap
							pair = (unvisited[neighbor][F_SCORE], id(neighbor))
							if pair not in unvisited_heap:
								heapq.heappush(unvisited_heap, (unvisited[neighbor][F_SCORE], id(neighbor)))
							

    			# Add current node to the visited list
				visited[current_node] = unvisited[current_node]
				
    			# Remove current node from the unvisited list
				del unvisited[current_node]

				# Get the unvisited node with the lowest f score value
				_, neighbor_id = heapq.heappop(unvisited_heap)

				# update current node to be the next node to be explored
				current_node = unvisited_neighbor_dict[neighbor_id]
	
	# trace the path from summit node to explorer node
	# and start printing maps from the explorer node				
	trace_and_print(visited, explorer_node, summit_node)

    # Return the final visited list
	return visited


# Test A* search function
result_map = a_star_search(graph_map, explorer_node, summit_node)

    

   
	