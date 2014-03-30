from term2048.board import Board
from time import sleep
from random import randrange

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
		print max(y for x in self.board.cells for y in x)
		sleep(.1)
		return self.__dirs[randrange(4)]