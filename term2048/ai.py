from term2048.board import Board
from time import sleep
from random import randrange, choice

class AI:
	__dirs = {
		0: Board.UP,
		1: Board.DOWN,
		2: Board.LEFT,
		3: Board.RIGHT,
	}
	
	def __init__(self, game):
		self.board = game.board

	def getMove(self):
		cells_remaining = {key: value for (key, value) in [(key, sum(1 for x in self.board.fake_move(self.__dirs[key]) if x == 0)) for key in self.__dirs]}

		inv_map = {}
		for k, v in cells_remaining.iteritems():
			inv_map[v] = inv_map.get(v, [])
			inv_map[v].append(k)

		sleep(.1)
		return self.__dirs[choice(inv_map[max(inv_map.keys())])]