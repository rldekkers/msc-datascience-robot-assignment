from Bot import *
from random import randint

class RandomBot(Bot):
	def __init__(self, settings):
		super().__init__(settings)
		self.possibleMoves = [UP, DOWN, RIGHT, LEFT]
		self.setName('Randy')
	
	def nextMove(self, currentCell, currentEnergy, vision, remainingStainCells):
		return self.possibleMoves[randint(0,3)]
