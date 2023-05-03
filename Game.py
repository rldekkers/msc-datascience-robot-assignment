import time
import os


class Game:
	def __init__(self, player, map, maxEnergy, latency, visuals, cls):
		self.map = map
		self.player = player
		self.energy = maxEnergy
		self.latency = latency
		self.visuals = visuals
		self.cls = cls

	def play(self):
		while self.energy>0 and self.map.remainingStains>0:
			nextMove = self.player.nextMove(self.map.botPosition, self.energy, self.map.getVision(), self.map.remainingStains)
			if nextMove and self.map.isValidMove(nextMove):
				self.map.moveRobot(nextMove)
				self.energy-=1
			else:
				self.energy-=1
			if self.visuals:
				self.map.printMap()
				print("Energy: ", self.energy, "\tStains left: ", self.map.remainingStains)
				self.map.printVision()
				print("Move made: ", nextMove)
			time.sleep(self.latency)
			if self.cls and self.visuals:
				os.system('cls' if os.name == 'nt' else 'clear')
		botName = getattr(self.player, 'name')
		if self.energy<=0:
			print("game over, " +botName+  " ran out of energy")
		elif self.map.remainingStains<=0:
			print(botName + " finished the map with a score of ", self.energy)

