from __future__ import print_function

import os
import os.path
import math

from colorama import init, Fore, Style
init(autoreset=True)

from term2048.board import Board

class Game(object):
	__clear = 'cls'

	COLORS = {
		1:  Fore.GREEN,
		2:  Fore.BLUE,
		3:  Fore.CYAN,
		4:  Fore.RED,
		5:  Fore.MAGENTA,
		6:  Fore.CYAN,
		7:  Fore.BLUE,
		8:  Fore.MAGENTA,
		9:  Fore.GREEN,
		10: Fore.RED,
		11: Fore.YELLOW,
		12: Fore.RED,
		13: Fore.CYAN,
	}

	def __init__(self, next_move, hidemode=False, **kws):
		self.board = Board(**kws)
		self.score = 0
		self.next_move = next_move
		self.hidemode = hidemode

	def incScore(self, pts):
		self.score += pts

	def end(self):
		return not (self.board.won() or self.board.canMove())

	def readMove(self):
		return self.next_move()

	def loop(self):
		while True:
			if not self.hidemode:
				os.system(Game.__clear)
				print(self.__str__(margins={'left': 4, 'top': 4, 'bottom': 4}))
			if self.board.won() or not self.board.canMove():
				break
			m = self.readMove()
			self.incScore(self.board.move(m))

		did_win = self.board.won()
		if not self.hidemode:
			print('You won!' if did_win else 'Game Over')
		return did_win, self.score

	def getCellStr(self, x, y):
		c = self.board.getCell(x, y)

		az = {}
		for i in range(1, int(math.log(self.board.goal(), 2))):
			az[2 ** i] = chr(i + 96)

		if c == 0:
			return '  .'
		elif c == 1024:
			s = ' 1k'
		elif c == 2048:
			s = ' 2k'
		else:
			s = '%3d' % c

		return self.COLORS.get(c, Fore.RESET) + s + Style.RESET_ALL

	def boardToString(self, margins={}):
		b = self.board
		rg = range(b.size())
		left = ' '*margins.get('left', 0)
		s = '\n'.join(
			[left + ' '.join([self.getCellStr(x, y) for x in rg]) for y in rg])
		return s

	def __str__(self, margins={}):
		b = self.boardToString(margins=margins)
		top = '\n'*margins.get('top', 0)
		bottom = '\n'*margins.get('bottom', 0)
		scores = ' \tScore: %5d\n' % self.score
		return top + b.replace('\n', scores, 1) + bottom
