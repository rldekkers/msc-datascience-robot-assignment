import csv
import random

CHECKPOINT_X = 1
CHECKPOINT_Y = 1

N_ROWS = 30
N_COLS = 30

N_STAINS = 3
SIZE_STAINS = 3

N_PILLARS = 3
SIZE_PILLARS = 3

N_WALLS = 3
SIZE_WALLS = 6

gameMap = []

def containsStuff(x,y):
	margin = max(SIZE_STAINS, SIZE_PILLARS)
	for i in range(x,x+margin):
		for j in range(y,y+margin):
			if gameMap[i][j] == '@' or gameMap[i][j] == 'x':
				return True
	return False

def crossesStuff(x,y,orientation):
	if orientation == 1:
		for j in range(y,y+SIZE_WALLS):
			if gameMap[x][j] == '@' or gameMap[x][j] == 'x':
				return True
	elif orientation == 2:
		for i in range(x,x+SIZE_WALLS):
			if gameMap[i][y] == '@' or gameMap[i][y] == 'x':
				return True
	return False

def generateStains():
	generatedStains = 0
	while generatedStains<N_STAINS:
		randX = random.randint(1,N_ROWS-SIZE_STAINS-1) #walls cannot contain stains (randX,randY is the top-left corner of the stain)
		randY = random.randint(1,N_COLS-SIZE_STAINS-1)
		
		if (randX==1 and randY==1) or  containsStuff(randX, randY):
			continue #don't want to cover the checkpoint or another stain or wall
		else:
			for i in range(randX, randX+SIZE_STAINS):
				for j in range(randY, randY+SIZE_STAINS):
					gameMap[i][j] = '@' #indicate stain
			generatedStains += 1

def generatePillars():
	generatedPillars = 0
	while generatedPillars<N_PILLARS:
		randX = random.randint(1,N_ROWS-SIZE_WALLS-1) #walls cannot contain pillars (randX,randY is the top-left corner of the stain)
		randY = random.randint(1,N_COLS-SIZE_WALLS-1)
		
		if (randX==1 and randY==1) or containsStuff(randX, randY):
			continue #don't want to cover the checkpoint or another stain or wall
		else:
			for i in range(randX, randX+SIZE_PILLARS):
				for j in range(randY, randY+SIZE_PILLARS):
					gameMap[i][j] = 'x' #indicate stain
			generatedPillars += 1

def generateWalls():
	generatedWalls = 0
	while generatedWalls<N_WALLS:
		orientation = random.randint(1,2) #1:horizontal, 2:vertical wall
		randX = random.randint(1,N_ROWS-SIZE_WALLS-1) #walls cannot contain pillars (randX,randY is the top-left corner of the stain)
		randY = random.randint(1,N_COLS-SIZE_WALLS-1)

		if orientation == 1:
			if(randX==1 and randY==1) or randY>=N_COLS-SIZE_WALLS or crossesStuff(randX, randY, orientation):
				continue
			else:
				for j in range(randY, randY+SIZE_WALLS):
					gameMap[randX][j] = 'x'
				generatedWalls += 1
		elif orientation == 2:
			if(randX==1 and randY==1) or randX>=N_ROWS-SIZE_WALLS or crossesStuff(randX, randY, orientation):
				continue
			else:
				for i in range(randX, randX+SIZE_WALLS):
					gameMap[i][randY] = 'x'
				generatedWalls += 1





for i in range(N_ROWS):
	row = []
	if i == 0 or i == N_ROWS-1:
		row = ['x' for x in range(N_COLS)]
		gameMap.append(row)
		continue
	for j in range(N_COLS):
		if j == 0 or j==N_COLS-1:
			row.append('x')
		else:
			row.append('.')
	gameMap.append(row)

gameMap[CHECKPOINT_X][CHECKPOINT_Y] = "#" #indicate checkpoint (vacuum spawn point)

generateStains()
generatePillars()
generateWalls()





csvFile = open('map1.csv', 'w', newline='')
writer = csv.writer(csvFile)

for line in gameMap:
	writer.writerow(line)
csvFile.close()
