from Bot import *

class Bot545046(Bot):

	# Initialize grid for storing memory of map
	def init_empty_map(self):
		return [['?' for col in range(self.settings['nrCols'])] for row in range(self.settings['nrRows'])]

	# Add outer walls to map
	def add_walls_to_map(self, map):
		for i in range(0, self.settings['nrCols']):
			map[0][i] = 'x'							 # upper
			map[self.settings['nrCols']-1][i] = 'x'	 # lower
		for j in range(0, self.settings['nrRows']):
			map[j][0] = 'x'							 # left
			map[j][self.settings['nrRows']-1] = 'x'	 # right
		return map

	# generate a list of exploration targets for A*, taking into account stainsize
	def generate_exploration_targets(self):
		
		return [[row, col] for col in range(1, self.settings['nrCols'] - 2, self.settings['sizeStains']) for row in range(1, self.settings['nrRows'] - 2, self.settings['sizeStains'])]

	def __init__(self, settings):
		super().__init__(settings)

		self.setName('Robertbot')
		self.settings = settings

		self.map_known = self.add_walls_to_map(self.init_empty_map())
		self.map_potential_stains = self.init_empty_map()

		self.locations_exploration_targets = self.generate_exploration_targets # tentative targets for A*
		self.locations_history = []  # note that back-tracking deletes visited cells!
		self.locations_stains = [] # store known stains

		self.path_a_star = [] # path which is currently begin traversed

		self.move_previous = "explore"

	def deepcopy_grid(self, grid):
		return [row[:] for row in grid]

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

	# rectilinear distance
	def dist_rect(self, cell_start, cell_end):
		# Manhattan distance = absolute horizontal dist. + abs. vert. dist.
		return abs(cell_end[0] - cell_start[0]) + abs(cell_end[1] - cell_start[1])

	# return dictionary with cell-coordinates of 4 adjacent cells, e.g. { "LEFT": [1,1], ... }
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
	def find_chars_in_grid(self, grid, char):
		return [[nRow, nCol] for nRow in range(0, len(grid)) for nCol in range(0, len(grid[nRow])) if grid[nRow][nCol] == char]

	# Convert location in vision to the corresponding location in the map
	def convert_loc_vision_to_map(self, cell_current, vision, loc_in_vision):
		# vision[1, 1] corresponds to map[cell_current[0], cell_current[1]]

		return [cell_current[0] + (loc_in_vision[0] - 1), cell_current[1] + (loc_in_vision[1] - 1)]






		pass

	# Determine move towards previous cell (according to 'location_history')
	def move_backtrack(self, currentCell):

		# delete current location and previous location
		# (when moved to previous location, this location will be appended to location_history by nextMove)
		del self.locations_history[-1:-3:-1]
		
		# find direction to get to previous cell
		return self.find_direction(currentCell, self.locations_history[-2])

	# Return move according to trajectory, which is as wide as possible without missing stains
	def move_explore_trajectory(self, currentCell):

		self.move_previous = "explore"

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

		self.move_previous = "explore"

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
				map_known_hyp = self.deepcopy_grid(self.map_known)

				# create fake vision
				vision_hyp = [['$' for i in range(3)] for j in range(3)]

				# add hypothetical vision after move to map
				map_known_hyp = self.add_vision_to_map(cell, vision_hyp, map_known_hyp)

				num_potential_stains = self.count_chars_in_grid(self.map_potential_stains, "?")

				# identify potential stains in hypothetical map
				map_potential_stains_hyp = self.deepcopy_grid(self.map_potential_stains)
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

	# used by 'get_path_a_star()'
	def reconstruct_path(self, came_from, cell_end):
		path = []
		cell_current = cell_end
		if tuple(cell_end) not in list(came_from.keys()): # correct?
			return [] # no path found
		
		# TEST!
		path.append(cell_end)

		while tuple(cell_current) in list(came_from.keys()):
			cell_current = came_from[tuple(cell_current)]
			path.insert(0, cell_current)

		del path[0]

		return path

	# TODO: return list of cells of path generated by A* algorithm
	def get_path_a_star(self, cell_start, cell_end):
	
		open_cells = []
		open_cells.append(cell_start)

		came_from = {}
		#came_from[tuple(cell_start)] = None

		g_cost_so_far = {} # { location: cost of cheapest known path}
		g_cost_so_far[tuple(cell_start)] = 0

		f_cost_so_far = {}

		while open_cells:

			if f_cost_so_far: open_cells.sort(key=lambda x: f_cost_so_far[tuple(x)])
		
			cell_current = open_cells[0] # cell with lowest f_cost

			if cell_current == cell_end:
				return self.reconstruct_path(came_from, cell_current)
			
			open_cells.remove(cell_current)

			# get those adjacent cells that are not obstacles or unknown cells
			adjacent_cells = [cell for cell in list(self.get_adjacent_cells(cell_current).values()) if (self.map_known[cell[0]][cell[1]] != "x" and self.map_known[cell[0]][cell[1]] != "?")]
			
			for cell_adjacent in adjacent_cells:  

				tentative_g_cost = g_cost_so_far[tuple(cell_current)] + self.dist_rect(cell_current, cell_adjacent)

				if tuple(cell_adjacent) not in g_cost_so_far or tentative_g_cost < g_cost_so_far[tuple(cell_adjacent)]:
					
					came_from[tuple(cell_adjacent)] = cell_current

					g_cost_so_far[tuple(cell_adjacent)] = tentative_g_cost
					f_cost_so_far[tuple(cell_adjacent)] = tentative_g_cost + self.dist_rect(cell_adjacent, cell_end)

					if cell_adjacent not in open_cells:
						open_cells.append(cell_adjacent)
						open_cells.sort(key = lambda x: f_cost_so_far[tuple(x)])
					
		return 0 # if goal never reached


		print("TO DO")
		return []

	# TODO: move towards tentative exploration targets. If target impossible, set new target
	def move_explore_a_star(self, cell_current):

		# if path not yet generated
		if not self.path_a_star:

			# select nearest exploration target
			# TODO: sorting by nearest ignores obstacles!
			self.locations_exploration_targets.sort(key = lambda x: self.dist_rect(cell_current, x))
			self.locations_stains[0]

			# generate path towards selected exploration target
			self.path_a_star = self.get_path_a_star(cell_current, self.locations_stains[0])



		# how to recognize target is impossible?

		# how to set new target?




		pass

	# TODO: revised 
	def move_stain_a_star(self, vision, cell_current):

		# if path not yet generated
		if not self.path_a_star:

			# select nearest stain
			# TODO: sorting by nearest ignores obstacles!
			self.locations_stains.sort(key = lambda x: self.dist_rect(cell_current, x))
			self.locations_stains[0]

			# generate path towards selected stain
			self.path_a_star = self.get_path_a_star(cell_current, self.locations_stains[0])

		# obtain first move
		move = self.find_direction(cell_current, self.path_a_star[0])

		# delete that cell from the path
		del self.path_a_star[0]

		return move


	def nextMove(self, currentCell, currentEnergy, vision, remainingStainCells):

		# update memory of map
		self.map_known = self.add_vision_to_map(currentCell, vision, self.map_known)

		#self.print_grid(self.map_known)

		# if stains in sight, add to list 'stain_locations'
		if self.count_chars_in_grid(vision, "@"):
			for location_vision in self.find_chars_in_grid(vision, "@"):
				location_map = self.convert_loc_vision_to_map(currentCell, vision, location_vision)
				if location_map not in self.locations_stains:
					self.locations_stains.append(location_map)
		
		# if stain visited, remove from list 'stain_locations'
		if currentCell in self.locations_stains:
			self.locations_stains.remove(currentCell)

		# TODO sort list by closest proximity to current location (ignores obstacles!)
		self.locations_stains.sort(key = lambda x: self.dist_rect(currentCell, x))

		# add current location to history (note that back-tracking deletes visited locations!)
		self.locations_history.append(currentCell.copy())

		# identify where stains might be
		self.map_potential_stains = self.identify_potential_stains(self.map_potential_stains, self.map_known)


		# if currentCell == [5, 5]:
		# 	test_path_a_star = self.get_path_a_star([6,2], [6,5])
		# 	print(test_path_a_star)
		# 	pass


		# TODO! currently, the bot creates a new A* path every move, forgetting about which stain it was targeting previously
		# Instead, it should complete the path to the stain until it is finished.

		if self.locations_stains:
			# clean up stain
			return self.move_stain_a_star(vision, currentCell)
		else:
			# explore
			return self.move_explore_dynamic(currentCell)
