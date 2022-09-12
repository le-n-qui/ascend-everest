# Node class

class Node(object):
	
	def __init__(self, x, y, z):
		self.x_pos = x
		self.y_pos = y
		self.elevation = z

	def get_x_pos(self):
		pass

	def get_y_pos(self):
		pass

	def get_z_pos(self):
		pass
		
	def print_node_info(self):
		print("X: ", self.x_pos)
		print("Y: ", self.y_pos)
		print("Z: ", self.elevation)



