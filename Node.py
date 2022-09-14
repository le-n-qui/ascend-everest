# Node class

class Node(object):
	
	def __init__(self, x, y, z):
		self.x_pos = x
		self.y_pos = y
		self.elevation = z

	def get_x_pos(self):
		return self.x_pos

	def get_y_pos(self):
		return self.y_pos

	def get_z_pos(self):
		return self.elevation
		
	def print_node_info(self):
		print("({}, {}, {})".format(self.x_pos, self.y_pos, self.elevation))
		



