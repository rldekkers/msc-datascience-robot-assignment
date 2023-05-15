from Bot import *

class Bot545046(Bot):

	# Initialize grid for storing memory of map
	def init_empty_map(self):
		empty_map = [['?' for col in range(self.settings['nrCols'])] for row in range(self.settings['nrRows'])]

		return empty_map

	# Add outer walls to map
	def add_walls_to_map(self, map):
		for i in range(0, self.settings['nrCols']):
			map[0][i] = 'x'							 # upper
			map[self.settings['nrCols']-1][i] = 'x'	 # lower
		for j in range(0, self.settings['nrRows']):
			map[j][0] = 'x'							 # left
			map[j][self.settings['nrRows']-1] = 'x'	 # right
		return map

	def __init__(self, settings):
		super().__init__(settings)

		self.setName('Robertbot')

		self.settings = settings

		self.map_known = self.add_walls_to_map(self.init_empty_map())
		self.map_potential_stains = self.init_empty_map()

		self.location_history = []  # note that back-tracking deletes visited cells!

		self.stain_locations = [] # store known stains

		self.move_stain_history = []
		self.last_move = "explore"

	def deepcopy(self, grid):
		return [row[:] for row in grid]

	# Add current vision to memory of map
	def add_vision_to_map(self, currentCell, vision, map):
		current_row = currentCell[0]
		current_col = currentCell[1]

		# store vision into knownMap
		map[current_row - 1][current_col - 1] = vision[0][0]
		map[current_row - 1][current_col    ] = vision[0][1]
		map[current_row - 1][current_col + 1] = vision[0][2]
		map[current_row    ][current_col - 1] = vision[1][0]
		map[current_row    ][current_col    ] = vision[1][1]
		map[current_row    ][current_col + 1] = vision[1][2]
		map[current_row + 1][current_col - 1] = vision[2][0]
		map[current_row + 1][current_col    ] = vision[2][1]
		map[current_row + 1][current_col + 1] = vision[2][2]

		return map

	# Print grid
	def print_grid(self, grid):
		for row in grid: print(''.join(row))
		print()

	# Find direction to move from cell_start to adjacent cell_end (not diagonal)
	def find_direction(self, cell_start, cell_end):
		if cell_end[0] < cell_start[0]:  # end is above start
			return UP
		elif cell_end[0] > cell_start[0]:  # end is below start
			return DOWN
		elif cell_end[1] > cell_start[1]:  # end is right of start
			return RIGHT
		elif cell_end[1] < cell_start[1]:  # end is left of start
			return LEFT

	# rectilinear distance from cell_start to cell_end
	def dist_rect(self, cell_start, cell_end):
		# Manhattan distance = absolute horizontal dist. + abs. vert. dist.
		return abs(cell_end[0] - cell_start[0]) + abs(cell_end[1] - cell_start[1])

	# return dictionary with cell-coordinates of 4 adjacent cells
	def get_adjacent_cells(self, cell_current):
		return {
				#       row                 column
				UP:    [cell_current[0] - 1, cell_current[1]    ],
				DOWN:  [cell_current[0] + 1, cell_current[1]    ],
				RIGHT: [cell_current[0]    , cell_current[1] + 1],
				LEFT:  [cell_current[0]    , cell_current[1] - 1]
			}
	
	# Identify all unexplored (!) locations where stains may exist, given memory (note that this ignores visible stains!)
	def identify_potential_stains(self, stains_map, known_map):

		# Make stainsMap blank
		for nRow in range(0, len(stains_map)):
			for nCol in range(0, len(stains_map)):
				stains_map[nRow][nCol] = '.'

		# iterate backwards through all cells of the stainsMap which can be the upper-left origin of an n*n stain
		for nRow in range(len(stains_map) - 1 - (self.settings['sizeStains'] - 1), -1, -1):
			for nCol in range(len(stains_map) - 1 - (self.settings['sizeStains'] - 1), -1, -1):

				only_question_marks = True

				for i in range(nRow, nRow + self.settings['sizeStains']):
					for j in range(nCol, nCol + self.settings['sizeStains']):

						if known_map[i][j] != "?":
							only_question_marks = False
							break  # stop checking

					if only_question_marks is False:
						break

				# stain possible
				if only_question_marks:
					for i in range(nRow, nRow + self.settings['sizeStains']):
						for j in range(nCol, nCol + self.settings['sizeStains']):
							stains_map[i][j] = "?"  # mark on map

		return stains_map

	# Return number of occurrences of char in grid (0 if none)
	def count_chars_in_grid(self, grid, char):
		return len([cell for row in grid for cell in row if cell == char])

	# Return locations of occurences of char in grid (empty list if none)
	# TODO: currently returns contents instead of coordinates
	def find_chars_in_grid(self, grid, char):
		return [[nRow, nCol] for nRow in range(0, len(grid)) for nCol in range(0, len(grid[nRow])) if grid[nRow][nCol] == char]

	# convert a location in vision to the corresponding location in the map
	def convert_loc_vision_to_map(self, current_cell, vision, loc_in_vision):
		# vision[1, 1] corresponds to map[current_cell[0], current_cell[1]]

		return [current_cell[0] + (loc_in_vision[0] - 1), current_cell[1] + (loc_in_vision[1] - 1)]






		pass

	# Generate move towards previous cell
	def move_backtrack(self, currentCell):

		# delete current location and previous location
		# (when moved to previous location, this location will be appended to location_history by nextMove)
		del self.location_history[-1:-3:-1]
		
		# find direction to get to previous cell
		return self.find_direction(currentCell, self.location_history[-2])

	# Return move according to trajectory, which is as wide as possible without missing stains
	def move_explore_trajectory(self, currentCell):

		self.last_move = "explore"

		current_row = currentCell[0]
		current_col = currentCell[1]

		size_stains = self.settings['sizeStains']
		d = size_stains + 2
		row_offset = 1

		print("🗑️🧹 Stain size: " + str(size_stains))

		# right
		if (current_row + row_offset) % (2 * d) == d and current_col != self.nrCols - (2 + size_stains):
			print("➡️  right")
			return RIGHT

		# down after right (corner)
		elif (current_row + row_offset) % (2 * d) == d and current_col == self.nrCols - (2 + size_stains):
			print("⬇️  down after right (corner)")
			return DOWN

		# down before left
		elif (current_row + row_offset) % (2 * d) != d and (current_row + row_offset) % (2 * d) != 0 and current_col == self.nrCols - (2 + size_stains):
			print("⬇️  down before left")
			return DOWN

		# left
		elif (current_row + row_offset) % (2 * d) == 0 and current_col != (1 + size_stains):
			print("⬅️  left")
			return LEFT

		# down after left (corner)
		elif (current_row + row_offset) % (2 * d) == 0 and current_col == (1 + size_stains):
			print("⬇️  down after left (corner)")
			return DOWN

		# down before right
		elif (current_row + row_offset) % (2 * d) != d and (current_row + row_offset) % (2 * d) != 0 and current_col == (1 + size_stains):
			print("⬇️  down before right")
			return DOWN

		# not on trajectory
		else:
			print("⬇️  ELSE")
			return DOWN

	# Generate move according to what will explore the most space
	def move_explore_dynamic(self, currentCell):

		self.last_move = "explore"

		adjacent_cells = self.get_adjacent_cells(currentCell)
		# {
		# 	#       row                 column
		# 	UP:    [currentCell[0] - 1, currentCell[1]    ],
		# 	DOWN:  [currentCell[0] + 1, currentCell[1]    ],
		# 	RIGHT: [currentCell[0]    , currentCell[1] + 1],
		# 	LEFT:  [currentCell[0]    , currentCell[1] - 1]
		# }

		def get_gain_per_direction(cell):
			gain = 0

			if self.map_known[cell[0]][cell[1]] == 'x':
				gain = 0  # an obstacle prevents the move
			else:
				# visualize explored territory in hypothetical map
				map_known_hyp = self.deepcopy(self.map_known)

				# create fake vision
				vision_hyp = [['$' for i in range(3)] for j in range(3)]

				# add hypothetical vision after move to map
				map_known_hyp = self.add_vision_to_map(cell, vision_hyp, map_known_hyp)

				num_potential_stains = self.count_chars_in_grid(self.map_potential_stains, "?")

				# identify potential stains in hypothetical map
				map_potential_stains_hyp = self.deepcopy(self.map_potential_stains)
				map_potential_stains_hyp = self.identify_potential_stains(map_potential_stains_hyp, map_known_hyp)

				# count number of potential stains after move
				hyp_potential_stains = self.count_chars_in_grid(map_potential_stains_hyp, "?")

				# compare
				gain = num_potential_stains - hyp_potential_stains


			return gain
		
		# calculate gain for all 4 adjacent directions
		gain_per_direction = {move: get_gain_per_direction(adjacent_cells[move]) for move in adjacent_cells}

		if gain_per_direction[max(gain_per_direction, key=gain_per_direction.get)] == 0:  # if nothing to gain

			# BUG: retracing steps does not guarantuee finding a new path! 

			return self.move_backtrack(currentCell)  # retrace steps
		else:
			# TODO: distinguish between multiple moves with the same gain-value
			return max(gain_per_direction, key=gain_per_direction.get)  # return move with largest gain-value

	# TO DO: return direction of first step in path (A*) from cell_start to cell_end, if possible
	# see https://www.youtube.com/watch?v=-L-WgKMFuhE 
	# see https://en.wikipedia.org/wiki/A*_search_algorith	m#Pseudocode 
	def move_path(self, cell_start, cell_end):

		# is cell_start or cell_end an obstacle?
		if self.map_known[cell_start[0]][cell_start[1]] == "x" or self.map_known[cell_end[0]][cell_end[1]] == "x":
			return 0

		# generate maps for storing f-cost per cell, and for storing visited cells
		map_path = self.deepcopy(self.map_known)
		map_visited = self.init_empty_map()

		# temporary storage for cost in each iteration (perhaps not necessary?)
		cost_per_direction = {
			UP: 0,
			DOWN: 0,
			RIGHT: 0,
			LEFT: 0
		}

		# start algorithm from cell_start
		cell_current = cell_start

		# f-cost of cell (based on distance to cell_start and cell_end)
		def get_f_cost(cell):
			# if cell is obstacle, cost is "x"
			if self.map_known[adjacent_cells[move][0]][adjacent_cells[move][1]] == "x":
				return "x"
			else: # else, return f-cost = g-cost (distance to start) + h-cost (distance to end)
				return self.dist_rect(cell_start, adjacent_cells[move]) + self.dist_rect(cell_end, adjacent_cells[move])
			
		# for every cell to evaluate (until path is found, or cannot be found)
		for i in range(0, 12): # for testing
		# while True:
			
			if cell_current == cell_end: break  # path found

			map_visited[cell_current[0]][cell_current[1]] = '!'  # note evaluated cell

			adjacent_cells = self.get_adjacent_cells(cell_current)

			# for every adjacent cell
			for move in adjacent_cells: 

				# Save f_cost in map_path
				map_path[adjacent_cells[move][0]][adjacent_cells[move][1]] = str(get_f_cost(adjacent_cells[move]))
		

			# ! TODO: prioritize unvisited cells over lower cells!!!
			# currently, lower cells are prioritized over unvisited cells



			# dict of cost-scores of adjacent cells, excluding obstacles, taken from map_path
			cost_per_direction = {move: int(map_path[adjacent_cells[move][0]][adjacent_cells[move][1]]) for move in adjacent_cells if map_path[adjacent_cells[move][0]][adjacent_cells[move][1]].isnumeric()}

			# find lowest value and filter out entries with higher value
			lowest_cost = min(cost_per_direction.values())
			cost_per_direction = {move: cost_per_direction[move] for move in cost_per_direction.keys() if cost_per_direction[move] == lowest_cost}
			
			if len(cost_per_direction) == 1:  # if only one option left, choose that one
				cell_current = adjacent_cells[list(cost_per_direction.items())[0][0]]
			elif len(cost_per_direction) > 1: # if multiple options left...
				
				# if un-visited cells left in options...
				if {move: cost_per_direction[move] for move in cost_per_direction if map_visited[adjacent_cells[move][0]][adjacent_cells[move][1]] != "!"}:
					# choose one of the not visited cells
					print("to do")

				# TODO: choose the one not visited yet
				# if all have been visited, choose the previous one?

				print("to do")

			# (temporary) simply assign one of the lowest values
			cell_current = adjacent_cells[min(cost_per_direction, key=cost_per_direction.get)] # choose cell with lowest cost (W.I.P.!)

		
		print("TO DO")

	# TO DO: Generate move to clean up stain in vision
	# consider the possibility that the bot encounters a 2nd stain while attempting to clean up the current one
	def move_stain(self, vision, currentCell, lastMove):

		self.last_move = "stain"

		print("TO DO")
		

	# TODO: Reconstruct path according to A* algorithm
	

	# TODO: A* algorithm with h=distance to goal
	# pseudocode
	# f-cost = g-cost + h-cost
	# g = dist. to start
	# h = dist. to end
	# def a_star(self, cell_start, cell_end):
		

	# 	def get_g_cost(cell_start, cell_current):  # dist. to start
	# 		return self.dist_rect(cell_start, cell_current)
	# 	def get_h_cost(cell_end, cell_current):  # dist. to end
	# 		return self.dist_rect(cell_end, cell_current)
	# 	def get_f_cost(cell_start, cell_current, cell_end):  # f-cost
	# 		return get_g_cost(cell_start, cell_current)+get_h_cost(cell_end, cell_current)

	# 	cells_open = [[cell_start,
	# 	 	get_g_cost(cell_start, cell_start),
	# 		get_f_cost(cell_start, cell_start, cell_end)]]
	# 	cells_closed = []

	# 	while cells_open:
	# 		cell_current = min(f_score, key=cells_open) # get cell for min. f_score
	# 		if cell_current == cell_end: pass # return reconstruct_path(came_from, current)
	# 		cells_open.remove(cell_current)
	# 		cells_closed.append(cell_current)
	# 		for cell_adjacent in self.get_adjacent_cells(cell_current):
	# 			if cell_adjacent in cells_closed or cell_adjacent == "x":
	# 				continue

	# 			tentative_g_cost = get_g_cost(cell_adjacent)
	# 			if tentative_g_score < g_score[cell_adjacent]:
	# 				came_from[cell_adjacent] = cell_current
	# 				f_score[cell_adjacent] = tentative_g_score + h_score
	# 				if cell_adjacent not in cells_open: cells_open.add(cell_adjacent)
	# 	return 0

		return LEFT

	# TODO: return list of cells of path generated by A* algorithm
	def get_path_a_star(self, cell_start, cell_end):



		print("TO DO")
		return []


	# TODO: revised 
	def move_stain2(self, vision, current_cell):

		# select cell to clean (the one most closeby to current cell)
		self.stain_locations[0]

		# generate path from current location to selected stain
		# path_to_stain = get_path_a_star(current_cell, self.stain_locations[0])

		# find direction to move to first upcoming location in path
		# direction_to_move =  self.find_direction(current_cell, path_to_stain[0])





		print("TO DO")
		return LEFT

	def nextMove(self, currentCell, currentEnergy, vision, remainingStainCells):

		# update memory of map
		self.map_known = self.add_vision_to_map(currentCell, vision, self.map_known)

		self.print_grid(self.map_known)

		# if stains in sight, add to list 'stain_locations'
		if self.count_chars_in_grid(vision, "@"):
			for location_vision in self.find_chars_in_grid(vision, "@"):
				location_map = self.convert_loc_vision_to_map(currentCell, vision, location_vision)
				if location_map not in self.stain_locations:
					self.stain_locations.append(location_map)
		
		# if stain visited, remove from list 'stain_locations'
		if currentCell in self.stain_locations:
			self.stain_locations.remove(currentCell)

		# TODO sort list by closest proximity to current location (ignores obstacles!)
		self.stain_locations.sort(key=lambda x: self.dist_rect(currentCell, x))

		# add current location to history (note that back-tracking deletes visited locations!)
		self.location_history.append(currentCell.copy())

		# identify where stains might be
		self.map_potential_stains = self.identify_potential_stains(self.map_potential_stains, self.map_known)

		# if no stains in memory, explore
		if self.stain_locations:
			# if stains in sight, clean up stain
			#return self.move_stain2(vision, currentCell)
			return self.move_explore_dynamic(currentCell)
		else:
			# if no stains in sight, explore
			return self.move_explore_dynamic(currentCell)
