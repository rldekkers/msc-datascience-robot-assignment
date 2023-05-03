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

		self.known_map = self.add_walls_to_map(self.init_empty_map())
		self.potential_stains_map = self.init_empty_map()

		self.move_stain_history = []
		self.last_move = "trajectory"

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
		for row in grid:
			print(''.join(row))
		print()

	# Identify all unexplored (!) locations where stains may exist, given memory (note that this ignores visible stains!)
	def identify_potential_stains(self, stains_map, known_map):

		# Start from a blank stainsMap
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

	# Return number of occurrences of char in current vision, if any (0 if none)
	def chars_in_grid(self, grid, char):
		num_chars = 0

		# count all occurrences of char
		for row in grid:
			for cell in row:
				if cell == char:
					num_chars += 1
		return num_chars

	# Generate move according to pre-determined trajectory, which is as wide as possible without missing stains
	def move_trajectory(self, currentCell):

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
	# TO DO: generate move in case all directions have gain=0
	def move_explore(self, currentCell, vision):

		# Gain depends on the number of potential stain-containing cells the move would exclude

		possible_cells = {
			#       row                 column
			UP:    [currentCell[0] - 1, currentCell[1]    ],
			DOWN:  [currentCell[0] + 1, currentCell[1]    ],
			RIGHT: [currentCell[0]    , currentCell[1] + 1],
			LEFT:  [currentCell[0]    , currentCell[1] - 1]
		}

		gain_per_direction = {
			UP: 0,
			DOWN: 0,
			RIGHT: 0,
			LEFT: 0
		}

		def get_gain_per_direction(cell):
			gain = 0

			if self.known_map[cell[0]][cell[1]] == 'x':
				gain = 0  # an obstacle prevents the move
			else:

				# visualize explored territory in hypothetical map
				hyp_known_map = self.deepcopy(self.known_map)

				# create fake vision
				hyp_vision = [['$' for i in range(3)] for j in range(3)]
				hyp_vision[1][1] = "\xC6"

				# add hypothetical vision after move to map
				hyp_known_map = self.add_vision_to_map(cell, hyp_vision, hyp_known_map)

				current_potential_stains = self.chars_in_grid(self.potential_stains_map, "?")

				hyp_potential_stains_map = self.deepcopy(self.potential_stains_map)

				# identify potential stains in hypothetical map
				hyp_potential_stains_map = self.identify_potential_stains(hyp_potential_stains_map, hyp_known_map)

				# count number of potential stains after move
				hyp_potential_stains = self.chars_in_grid(hyp_potential_stains_map, "?")

				# compare
				gain = current_potential_stains - hyp_potential_stains

			return gain

		# iterate through all 4 possible moves
		for move in possible_cells:
			gain_per_direction[move] = get_gain_per_direction(possible_cells[move])

		# print()
		# print("Cells that would be excluded from containing stains:")
		# print("     " + str(gain_per_direction["up"]) + "    ")
		# print("     ↑     ")
		# print(str(gain_per_direction["left"]) + " ←  \xC6  → " + str(gain_per_direction["right"]))
		# print("     ↓     ")
		# print("     " + str(gain_per_direction["down"]) + "    ")
		# print("Best movement: " + str(max(gain_per_direction, key=gain_per_direction.get)))
		# print()

		# return move with largest gain-value
		return max(gain_per_direction, key=gain_per_direction.get)

	# TO DO: Generate move to clean up stain in vision
	def move_stain(self, vision, currentCell, lastMove):

		# Keep history of moves since encountering first stain-cell
		if lastMove != "stain":
			self.move_stain_history = []
		self.move_stain_history.append(currentCell.copy())

		print()
		print("moveStainHistory: ")
		for i in range(0, len(self.move_stain_history)):
			print(str(i) + ":  " + str(self.move_stain_history[i]))

		# once encountered, if not at corner of stain, initiate move to corner of stain

		# if not at corner of stain, move to corner of stain

		print("to do")

	# TO DO: Generate move to get around obstacle
	def move_obstacle(self, vision, currentCell, lastMove):
		print("to do")

	def nextMove(self, currentCell, currentEnergy, vision, remainingStainCells):

		self.known_map = self.add_vision_to_map(currentCell, vision, self.known_map)
		self.potential_stains_map = self.identify_potential_stains(self.potential_stains_map, self.known_map)

		# print("🧠  Robot-memory:")
		# self.print_grid(self.knownMap)

		# print("🔎  Potential stains:")
		# self.print_grid(self.potentialStainsMap)

		if self.chars_in_grid(vision, "@") is False and self.chars_in_grid(vision, "x") is False:
			self.last_move = "trajectory"

		if self.chars_in_grid(vision, "@"):
			print("🗑️🧹 Stains in sight: " + str(self.chars_in_grid(vision, "@")))
			# currentMove = self.move_stain(vision, currentCell, self.lastMove)
			# self.lastMove = "stain"
			# return currentMove

		if self.chars_in_grid(vision, "x"):
			print("🚧⛔ Obstacles in sight: " + str(self.chars_in_grid(vision, "x")))
			# currentMove = self.move_obstacle(vision, currentCell, self.lastMove)
			# self.lastMove = "obstacle"
			# return currentMove

		return self.move_explore(currentCell, vision)
