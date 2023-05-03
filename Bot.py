UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

class Bot:
	
	def __init__(self, settings):
		self.nrCols = settings['nrCols']
		self.nrRows = settings['nrRows']
		self.nrStains = settings['nrStains']
		self.nrPillars = settings['nrPillars']
		self.nrWalls = settings['nrWalls']
		self.sizeStains = settings['sizeStains']
		self.sizePillars = settings['sizePillars']
		self.sizeWalls = settings['sizeWalls']
		self.checkpoint = settings['checkpoint']


	def nextMove(self, currentCell, currentEnergy, vision, remainingStainCells):
		raise NotImplementedError
		
	def setName(self, name):
		self.name = name

