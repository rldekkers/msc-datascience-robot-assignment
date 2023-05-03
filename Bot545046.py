from Bot import *

class Bot545046(Bot):

	# Initialize grid for storing memory of map
	def initEmptyMap(self):
		emptyMap = [['?' for i in range(self.settings['nrCols'])]
		   for j in range(self.settings['nrRows'])]
		
		return emptyMap
	
	# Add outer walls to map
	def addWallsToMap(self, map):

		for i in range(0, self.settings['nrCols']): 
			map[0][i] = 'x'							# upper
			map[self.settings['nrCols']-1][i] = 'x'	# lower

		for j in range(0, self.settings['nrRows']):
			map[j][0] = 'x'							# left
			map[j][self.settings['nrRows']-1] = 'x'	# right

		return map

	def __init__(self, settings):
		super().__init__(settings)

		self.setName('Robertbot')

		self.settings = settings

		self.knownMap = self.addWallsToMap(self.initEmptyMap())

		self.potentialStainsMap = self.initEmptyMap()

		self.lastMove = "trajectory"

	def deepCopy(self, grid):
		return [row[:] for row in grid]

	# Add current vision to memory of map
	def addVisionToMap(self, currentCell, vision, map):
		currentRow = currentCell[0]
		currentCol = currentCell[1]

		# store vision into knownMap
		map[currentRow - 1][currentCol - 1] = vision[0][0]
		map[currentRow - 1][currentCol    ] = vision[0][1]
		map[currentRow - 1][currentCol + 1] = vision[0][2]
		map[currentRow    ][currentCol - 1] = vision[1][0]
		map[currentRow    ][currentCol    ] = vision[1][1]
		map[currentRow    ][currentCol + 1] = vision[1][2]
		map[currentRow + 1][currentCol - 1] = vision[2][0]
		map[currentRow + 1][currentCol    ] = vision[2][1]
		map[currentRow + 1][currentCol + 1] = vision[2][2]

		return map

	# Print grid
	def printGrid(self, grid):
		for row in grid:
			print(''.join(row))
		print()

	# Identify all unexplored (!) locations where stains may exist, given memory (note that this ignores visible stains!)
	def identifyPotentialStains(self, stainsMap, knownMap):
				
		# Start from a blank stainsMap
		for nRow in range(0, len(stainsMap)):
			for nCol in range(0, len(stainsMap)):
				stainsMap[nRow][nCol] = '.'

		# iterate backwards through all cells of the stainsMap which can be the upper-left origin of a n*n stain
		for nRow in range(len(stainsMap) - 1 - (self.settings['sizeStains'] - 1), -1, -1):
			for nCol in range(len(stainsMap) - 1 - (self.settings['sizeStains'] - 1), -1, -1):

				onlyQuestionMarks = True

				for i in range(nRow, nRow + self.settings['sizeStains']):
					for j in range(nCol, nCol + self.settings['sizeStains']):

						if knownMap[i][j] != "?":
							onlyQuestionMarks = False
							break # stop checking
				
					if onlyQuestionMarks == False:
						break

				# stain possible
				if onlyQuestionMarks == True:
					for i in range(nRow, nRow + self.settings['sizeStains']):
						for j in range(nCol, nCol + self.settings['sizeStains']):
							stainsMap[i][j] = "?" # mark on map

		return stainsMap

	# Return number of occurences of char in current vision, if any (0 if none)
	def charsInGrid(self, grid, char):
		nChars = 0

		# count all occurences of char
		for row in grid:
			for cell in row:
				if cell == char:
					nChars += 1
		return nChars

	# Generate move according to pre-determined trajectory, which is as wide as possible without missing stains
	def moveTrajectory(self, currentCell):

		currentRow = currentCell[0]
		currentCol = currentCell[1]
		
		sizeStains = self.settings['sizeStains']
		d = sizeStains + 2
		rowOffset = 1

		print("🗑️🧹 Stainsize: " + str(sizeStains))

		# right
		if (currentRow+rowOffset)%(2*d) == d and currentCol != self.nrCols - (2 + sizeStains):
			print("➡️  right")
			return RIGHT
		
		# down after right (corner)
		elif (currentRow+rowOffset)%(2*d) == d and currentCol == self.nrCols - (2 + sizeStains):
			print("⬇️  down after right (corner)")
			return DOWN

		# down before left
		elif (currentRow+rowOffset)%(2*d) != d and (currentRow+rowOffset)%(2*d) != 0 and currentCol == self.nrCols - (2 + sizeStains):
			print("⬇️  down before left")
			return DOWN

		# left
		elif (currentRow+rowOffset)%(2*d) == 0 and currentCol != (1 + sizeStains):
			print("⬅️  left")
			return LEFT
		
		# down after left (corner)
		elif (currentRow+rowOffset)%(2*d) == 0 and currentCol == (1 + sizeStains):
			print("⬇️  down after left (corner)")
			return DOWN
		
		# down before right
		elif (currentRow+rowOffset)%(2*d) != d and (currentRow+rowOffset)%(2*d) != 0 and currentCol == (1 + sizeStains):
			print("⬇️  down before right")
			return DOWN

		# not on trajectory
		else:
			print("⬇️  ELSE")
			return DOWN
		
	# Generate move according to what will explore the most space
	# TO DO: generate move in case all directions have gain=0
	def moveExplore(self, currentCell, vision):

		# Gain is a function of the number of currently unexplored cells that could contain a stain, which will be in the vision after the move
		
		possibleCells = {
			#       row                 column
			UP:    [currentCell[0] - 1, currentCell[1]    ],
			DOWN:  [currentCell[0] + 1, currentCell[1]    ],
			RIGHT: [currentCell[0]    , currentCell[1] + 1],
			LEFT:  [currentCell[0]    , currentCell[1] - 1]
		}

		gainPerDirection = {
			UP: 0,
			DOWN: 0,
			RIGHT: 0,
			LEFT: 0
		}

		def getGainPerDirection(cell):
			gain = 0

			if self.knownMap[cell[0]][cell[1]] == 'x':
				gain = 0 # an obstacle prevents the move
			else:

				# visualize explored territory in hypothetical map
				hypotheticalKnownMap = self.deepCopy(self.knownMap)

				# create fake vision
				hypotheticalVision = [['$' for i in range(3)] for j in range(3)]
				hypotheticalVision[1][1] = "\xC6"

				# add hypothetical vision after move to map
				hypotheticalKnownMap = self.addVisionToMap(cell, hypotheticalVision, hypotheticalKnownMap)

				potentialStainsCurrent = self.charsInGrid(self.potentialStainsMap, "?")

				hypotheticalPotentialStainsMap = self.deepCopy(self.potentialStainsMap)

				# identify potential stains in hypothetical map
				hypotheticalPotentialStainsMap = self.identifyPotentialStains(hypotheticalPotentialStainsMap, hypotheticalKnownMap)
				
				# count number of potential stains after move
				potentialStainsNew = self.charsInGrid(hypotheticalPotentialStainsMap, "?")

				# compare
				gain = potentialStainsCurrent - potentialStainsNew

			return gain
		
		# iterate through all 4 possible moves
		for move in possibleCells:
			gainPerDirection[move] = getGainPerDirection(possibleCells[move])

		# print()
		# print("Cells that would be excluded from containing stains:")
		# print("     " + str(gainPerDirection["up"]) + "    ")
		# print("     ↑     ")
		# print(str(gainPerDirection["left"]) + " ←  \xC6  → " + str(gainPerDirection["right"]))
		# print("     ↓     ")
		# print("     " + str(gainPerDirection["down"]) + "    ")
		# print("Best movement: " + str(max(gainPerDirection, key=gainPerDirection.get)))
		# print()

		# return move with largest gain-value
		return max(gainPerDirection, key=gainPerDirection.get)


	# TO DO: Generate move to clean up stain in vision
	def moveStain(self, vision, currentCell, lastMove):

		# Keep history of moves since encountering first stain-cell
		if lastMove != "stain":
			self.moveStainHistory = []
		self.moveStainHistory.append(currentCell.copy())

		print()
		print("moveStainHistory: ")
		for i in range(0, len(self.moveStainHistory)):
			print(str(i) + ":  " + str(self.moveStainHistory[i]))
		
		
		# once encountered, if not at corner of stain, initiate move to corner of stain


		# if not at corner of stain, move to corner of stain







		print("to do")

	# TO DO: Generate move to get around obstacle
	def moveObstacle(self, vision, currentCell, lastMove):
		print("to do")

	def nextMove(self, currentCell, currentEnergy, vision, remainingStainCells):
		
		self.knownMap           = self.addVisionToMap(currentCell, vision, self.knownMap)
		self.potentialStainsMap = self.identifyPotentialStains(self.potentialStainsMap, self.knownMap)

		# print("🧠  Robot-memory:")
		# self.printGrid(self.knownMap)

		# print("🔎  Potential stains:")
		# self.printGrid(self.potentialStainsMap)
		
		if self.charsInGrid(vision, "@") == False and self.charsInGrid(vision, "x") == False:
			self.lastMove = "trajectory"

		if self.charsInGrid(vision, "@"):
			print("🗑️🧹 Stains in sight: " + str(self.charsInGrid(vision, "@")))
			#currentMove = self.moveStain(vision, currentCell, self.lastMove)
			#self.lastMove = "stain"
			# return currentMove

		if self.charsInGrid(vision, "x"):
			print("🚧⛔ Obstacles in sight: " + str(self.charsInGrid(vision, "x")))
			# currentMove = self.moveObstacle(vision, currentCell, self.lastMove)
			# self.lastMove = "obstacle"
			# return currentMove

		return self.moveExplore(currentCell, vision) 