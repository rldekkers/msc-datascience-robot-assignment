import csv
import os


class Map:
	def __init__(self, settings):
		self.map = self.readMapFile(settings['mapName'])
		self.nrCols = settings['nrCols']
		self.nrRows = settings['nrRows']
		self.nrStains = settings['nrStains']
		self.nrPillars = settings['nrPillars']
		self.nrWalls = settings['nrWalls']
		self.sizeStains = settings['sizeStains']
		self.sizePillars = settings['sizePillars']
		self.sizeWalls = settings['sizeWalls']
		self.checkpoint = settings['checkpoint']
		self.remainingStains = (self.sizeStains**2)*self.nrStains #size of a stain * nr of stains
		self.botPosition = self.checkpoint[:] #bot always starts at the checkpoint

	def readMapFile(self, mapPath):
		mapFile = open(mapPath, 'r')
		reader = csv.reader(mapFile, delimiter=',')
		return list(reader)

	def getVision(self):
		vision = []
		for i in range(self.botPosition[0]-1,self.botPosition[0]+2):
			row = []
			for j in range(self.botPosition[1]-1,self.botPosition[1]+2):
				row.append(self.map[i][j])
			vision.append(row)
		return vision

	def printVision(self):
		vision = self.getVision()
		# print(vision)
		for line in vision:
			print(''.join(line))

	def isValidMove(self, move):
		if move == 'up':
			if self.map[self.botPosition[0]-1][self.botPosition[1]] != 'x':
				return True
		elif move == 'down':
			if self.map[self.botPosition[0]+1][self.botPosition[1]] != 'x':
				return True
		elif move == 'left':
			if self.map[self.botPosition[0]][self.botPosition[1]-1] != 'x':
				return True
		elif move == 'right':
			if self.map[self.botPosition[0]][self.botPosition[1]+1] != 'x':
				return True
		return False

	def moveRobot(self, move):
		currentPosition = self.botPosition[:]
		if move == 'up':
			self.botPosition[0] = self.botPosition[0]-1
			if self.map[self.botPosition[0]][self.botPosition[1]] == '@':
				self.remainingStains -=1
		elif move == 'down':
			self.botPosition[0] = self.botPosition[0]+1
			if self.map[self.botPosition[0]][self.botPosition[1]] == '@':
				self.remainingStains -=1
		elif move == 'left':
			self.botPosition[1] = self.botPosition[1]-1
			if self.map[self.botPosition[0]][self.botPosition[1]] == '@':
				self.remainingStains -=1
		elif move == 'right':
			self.botPosition[1] = self.botPosition[1]+1
			if self.map[self.botPosition[0]][self.botPosition[1]] == '@':
				self.remainingStains -=1

		self.map[self.botPosition[0]][self.botPosition[1]] = '\xC6'
		if currentPosition == self.checkpoint:
			self.map[currentPosition[0]][currentPosition[1]] = '#'
		else:
			self.map[currentPosition[0]][currentPosition[1]] = '.'



	def printMap(self):
		for line in self.map:
			print(''.join(line))

