from Bot import *

class BruteBot(Bot):
	def __init__(self, settings):
		super().__init__(settings)
		self.setName('Brutus')
		
	
	def nextMove(self, currentCell, currentEnergy, vision, remainingStainCells):
		if currentCell[0]%2 == 1 and currentCell[1] != self.nrCols-2:
			return RIGHT
		elif currentCell[0]%2 == 1 and currentCell[1] == self.nrCols-2:
			return DOWN
		elif currentCell[0]%2 == 0 and currentCell[1] != 1:
			return LEFT
		elif currentCell[0]%2 == 0 and currentCell[1] == 1:
			return DOWN