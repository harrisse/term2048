import msvcrt
from msvcrt import getch
from term2048.board import Board

class Player:
	__dirs = {
		72: Board.UP,
		80: Board.DOWN,
		75: Board.LEFT,
		77: Board.RIGHT,
	}

	def getMove(self):
		while True:
			if msvcrt.kbhit():
				if ord(getch()) == 224:
					return self.__dirs[ord(getch())]