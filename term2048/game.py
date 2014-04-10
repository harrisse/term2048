from __future__ import print_function

import os
import os.path
import math

from colorama import init, Fore, Style
init(autoreset=True)

from term2048.player import Player
from term2048.board import Board

class Game(object):
	__clear = 'cls' if os.name == 'nt' else 'clear'

	COLORS = {
		2:    Fore.GREEN,
		4:    Fore.BLUE,
		8:    Fore.CYAN,
		16:   Fore.RED,
		32:   Fore.MAGENTA,
		64:   Fore.CYAN,
		128:  Fore.BLUE,
		256:  Fore.MAGENTA,
		512:  Fore.GREEN,
		1024: Fore.RED,
		2048: Fore.YELLOW,
		4096: Fore.RED,
		8192: Fore.CYAN,
	}

	SCORES_FILE = '%s/.term2048.scores' % os.path.expanduser('~')

	def __init__(self, ai=None, hidemode=False, **kws):
		self.board = Board(**kws)
		self.score = 0
		self.scores_file = self.SCORES_FILE
		self.movepicker = ai if ai is not None else Player()

		self.__hidemode = hidemode

		self.loadBestScore()

	def loadBestScore(self):
		if self.scores_file is None or not os.path.exists(self.scores_file):
			self.best_score = 0
			return
		try:
			f = open(self.scores_file, 'r')
			self.best_score = int(f.readline(), 10)
			f.close()
		except:
			pass

	def saveBestScore(self):
		if self.score > self.best_score:
			self.best_score = self.score
		try:
			f = open(self.scores_file, 'w')
			f.write(str(self.best_score))
			f.close()
		except:
			pass

	def incScore(self, pts):
		self.score += pts
		if self.score > self.best_score:
			self.best_score = self.score

	def end(self):
		return not (self.board.won() or self.board.canMove())

	def readMove(self):
		return self.movepicker.getMove()

	def loop(self):
		try:
			while True:
				if not self.__hidemode:
					os.system(Game.__clear)
					print(self.__str__(margins={'left': 4, 'top': 4, 'bottom': 4}))
				if self.board.won() or not self.board.canMove():
					break
				m = self.readMove()
				self.incScore(self.board.move(m))

		except KeyboardInterrupt:
			self.saveBestScore()
			return

		self.saveBestScore()
		did_win = self.board.won()
		if not self.__hidemode:
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
		scores = ' \tScore: %5d  Best: %5d\n' % (self.score, self.best_score)
		return top + b.replace('\n', scores, 1) + bottom
