from Map import Map
from Bot import Bot
from Game import Game
import importlib
import traceback



# settings = {
# 	'mapName' : "map1.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 3,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "map2.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 2,
# 	'nrWalls' : 3,
# 	'sizeStains' : 3,
# 	'sizePillars' : 3,
# 	'sizeWalls' : 6,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "map3.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 1,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_6_30_1_3_0_0_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 1,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 3,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_6_30_3_3_0_0_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 3,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_6_30_5_3_0_0_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 5,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 3,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_6_30_10_3_0_0_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 10,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 3,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_7_15_20_1_0_0_0_0_.csv",
# 	'nrCols' : 15,
# 	'nrRows' : 15,
# 	'nrStains' : 20,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 1,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_7_30_1_5_0_0_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 1,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 5,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_7_30_5_1_0_0_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 5,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 1,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_7_30_30_2_0_0_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 30,
# 	'nrPillars' : 0,
# 	'nrWalls' : 0,
# 	'sizeStains' : 2,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_8_20_3_1_5_3_0_0_.csv",
# 	'nrCols' : 20,
# 	'nrRows' : 20,
# 	'nrStains' : 3,
# 	'nrPillars' : 5,
# 	'nrWalls' : 0,
# 	'sizeStains' : 1,
# 	'sizePillars' : 3,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_8_30_1_1_3_7_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 1,
# 	'nrPillars' : 3,
# 	'nrWalls' : 0,
# 	'sizeStains' : 1,
# 	'sizePillars' : 5,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_8_30_1_3_10_3_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 1,
# 	'nrPillars' : 10,
# 	'nrWalls' : 0,
# 	'sizeStains' : 3,
# 	'sizePillars' : 3,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_8_30_3_3_3_3_0_0_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 3,
# 	'nrWalls' : 0,
# 	'sizeStains' : 3,
# 	'sizePillars' : 3,
# 	'sizeWalls' : 0,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_9_30_1_3_1_3_15_3_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 1,
# 	'nrPillars' : 1,
# 	'nrWalls' : 15,
# 	'sizeStains' : 3,
# 	'sizePillars' : 3,
# 	'sizeWalls' : 3,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_9_30_1_3_1_3_15_3_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 1,
# 	'nrPillars' : 1,
# 	'nrWalls' : 15,
# 	'sizeStains' : 3,
# 	'sizePillars' : 3,
# 	'sizeWalls' : 3,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_9_30_3_1_5_4_5_8_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 5,
# 	'nrWalls' : 5,
# 	'sizeStains' : 1,
# 	'sizePillars' : 4,
# 	'sizeWalls' : 8,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_9_30_3_3_3_3_3_5_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 3,
# 	'nrWalls' : 3,
# 	'sizeStains' : 3,
# 	'sizePillars' : 3,
# 	'sizeWalls' : 5,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_9_30_10_3_1_5_3_15_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 10,
# 	'nrPillars' : 1,
# 	'nrWalls' : 3,
# 	'sizeStains' : 3,
# 	'sizePillars' : 5,
# 	'sizeWalls' : 15,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_10_30_1_1_0_0_80_3_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 1,
# 	'nrPillars' : 0,
# 	'nrWalls' : 80,
# 	'sizeStains' : 1,
# 	'sizePillars' : 0,
# 	'sizeWalls' : 3,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_10_30_3_3_1_4_40_6_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 1,
# 	'nrWalls' : 40,
# 	'sizeStains' : 3,
# 	'sizePillars' : 4,
# 	'sizeWalls' : 6,
# 	'checkpoint' : [1,1],
# }

# settings = {
# 	'mapName' : "maps\map_10_30_3_3_25_2_25_3_.csv",
# 	'nrCols' : 30,
# 	'nrRows' : 30,
# 	'nrStains' : 3,
# 	'nrPillars' : 25,
# 	'nrWalls' : 25,
# 	'sizeStains' : 3,
# 	'sizePillars' : 2,
# 	'sizeWalls' : 3,
# 	'checkpoint' : [1,1],
# }

settings = {
	'mapName' : "maps\map_10_30_40_1_40_2_0_0_.csv",
	'nrCols' : 30,
	'nrRows' : 30,
	'nrStains' : 40,
	'nrPillars' : 40,
	'nrWalls' : 0,
	'sizeStains' : 1,
	'sizePillars' : 2,
	'sizeWalls' : 0,
	'checkpoint' : [1,1],
}

MAX_STEPS = 1000
LATENCY = .05
VISUALS = True
CLS = True

botName = 'Bot545046'
module = importlib.import_module(botName)
cls = getattr(module, botName)

myMap = Map(settings)
bot = cls(settings)
if not getattr(bot, 'name', False):
	bot.setName(botName)
game = Game(bot, myMap, MAX_STEPS, LATENCY, VISUALS, CLS)


try:
	game.play()
except Exception:
	print("Encountered error: ", traceback.format_exc())