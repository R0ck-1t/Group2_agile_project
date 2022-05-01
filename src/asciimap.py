from math import floor
class AsciiMap:
	"""map printing and computing"""
	#constructor that takes dimension list and file name
	def __init__(self, dimensions, file_name):
		self.file_name = file_name
		self.dimensions = dimensions
		#uses encoding to read special characters
		with open(self.file_name, encoding="utf-8") as file:
			lines = file.readlines()
		self.tiles = []
		stripped_lines = []
		for line in lines:
			stripped_lines.append(line.rstrip())
		self.length_of_tile = round(len(stripped_lines[0]) / self.dimensions[0])
		for new_line in stripped_lines:
			self.tiles.append([str(new_line[i:i+self.length_of_tile]) for i in range(0, len(new_line), self.length_of_tile)])
		
	
	#method that prints map
	def __repr__(self):
		for line in self.tiles:
			#uses str to print special characters
			print(str(line))
		#keeps __repr__ from getting angie, needs to be fed
		return ""

	def print_tiles(self, coordinates):
		y = coordinates[0]
		x = coordinates[1]
		tile_layers = [[x-1, y-1], [x, y-1], [x+1, y-1], [x-1, y], [x, y], [x+1, y], [x-1, y+1], [x, y+1], [x+1, y+1]]
		tiles_list = []
		line_count = len(self.tiles) / self.dimensions[1]
		remainder = line_count % 1
		line_count = floor(line_count)
		for coord in tile_layers:
			x_convert = coord[0] - 1
			y_convert = (coord[1] - 1) * line_count
			every_extra_line_at = round(1 / remainder)
			if (x_convert < 0) or (y_convert < 0) or (x_convert >= self.dimensions[0]) or (coord[1] >= self.dimensions[1]):
				tile_string = " " * self.length_of_tile
				if (y // every_extra_line_at) == 0:
					tile = [tile_string, tile_string, tile_string, tile_string]
				else:
					tile = [tile_string, tile_string, tile_string]
				tiles_list.append(tile)
			else:
				tile = []
				if (y_convert // every_extra_line_at) == 0: #more lines than normal
					for i in range(0, line_count + 1):
						#print("X " + str(x_convert + i))
						#print("Y " + str(y_convert + i))
						tile.append(self.tiles[y_convert + i][x_convert])
				else:	#normal amt of lines
					for i in range(0, line_count):
						#print("X " + str(x_convert + i))
						#print("Y " + str(y_convert + i))
						tile.append(self.tiles[y_convert + i][x_convert])
				tiles_list.append(tile)
		layer1 = [tiles_list[0], tiles_list[1], tiles_list[2]]
		layer2 = [tiles_list[3], tiles_list[4], tiles_list[5]]
		layer3 = [tiles_list[6], tiles_list[7], tiles_list[8]]

		return_string = "+" * (self.length_of_tile * 3)
		return_string += "++\n"
		last_string = return_string
		for i in range(0, len(layer1[0])):
			tile = "+"
			for tiles_list in layer1:
				tile += tiles_list[i]
			return_string += tile + "+\n"
		for i in range(0, len(layer2[0])):
			tile = "+"
			for tiles_list in layer2:
				tile += tiles_list[i]
			return_string += tile + "+\n"
		for i in range(0, len(layer3[0])):
			tile = "+"
			for tiles_list in layer3:
				tile += tiles_list[i]
			return_string += tile + "+\n"
		return_string += last_string
		return return_string
		


		
		



	def tiles(self):
		tile_list = []
		tile_list_index = 0
		for line in self.line_list:
			#makes list inside list
			tile_list.append([])
			count = 0
			tile = ""
			for char in line:
				count += 1
				tile += char
				if (count % round(len(line)/self.dimensions[1])) == 0:
					tile_list[tile_list_index].append(tile)
					tile = ""
			if tile != "":
				tile_list[tile_list_index].append(tile)
			tile_list_index += 1
		self.tile_list = tile_list

	def tile_display(self):
		for i in self.tile_list:
			word = ""
			for tile in i:
				word += tile
				word += "-"
			print(str(word))

