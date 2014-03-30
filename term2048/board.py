import random

try:
	xrange
except NameError:
	xrange = range

class Board(object):
	UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

	GOAL = 2048
	SIZE = 4

	def __init__(self, goal=GOAL, size=SIZE, **kws):
		self.__size = size
		self.__size_range = xrange(0, self.__size)
		self.__goal = goal
		self.__won = False
		self.cells = [[0]*self.__size for _ in xrange(self.__size)]
		self.addTile()
		self.addTile()

	def size(self):
		return self.__size

	def goal(self):
		return self.__goal

	def won(self):
		return self.__won

	def canMove(self):
		if not self.filled():
			return True

		for y in self.__size_range:
			for x in self.__size_range:
				c = self.getCell(x, y)
				if (x < self.__size-1 and c == self.getCell(x+1, y)) \
				   or (y < self.__size-1 and c == self.getCell(x, y+1)):
					return True

		return False

	def filled(self):
		return len(self.getEmptyCells()) == 0

	def addTile(self, value=None, choices=([2]*9+[4])):
		if value:
			choices = [value]

		v = random.choice(choices)
		empty = self.getEmptyCells()
		if empty:
			x, y = random.choice(empty)
			self.setCell(x, y, v)

	def getCell(self, x, y):
		return self.cells[y][x]

	def setCell(self, x, y, v):
		self.cells[y][x] = v

	def getLine(self, y):
		return self.cells[y]

	def getCol(self, x):
		return [self.getCell(x, i) for i in self.__size_range]

	def setLine(self, y, l):
		self.cells[y] = l[:]

	def setCol(self, x, l):
		for i in xrange(0, self.__size):
			self.setCell(x, i, l[i])

	def getEmptyCells(self):
		return [(x, y)
				for x in self.__size_range
				for y in self.__size_range if self.getCell(x, y) == 0]

	def __collapseLineOrCol(self, line, d):
		if (d == Board.LEFT or d == Board.UP):
			inc = 1
			rg = xrange(0, self.__size-1, inc)
		else:
			inc = -1
			rg = xrange(self.__size-1, 0, inc)

		pts = 0
		for i in rg:
			if line[i] == 0:
				continue
			if line[i] == line[i+inc]:
				v = line[i]*2
				if v == self.__goal:
					self.__won = True

				line[i] = v
				line[i+inc] = 0
				pts += v

		return (line, pts)

	def __moveLineOrCol(self, line, d):
		nl = [c for c in line if c != 0]
		if d == Board.UP or d == Board.LEFT:
			return nl + [0] * (self.__size - len(nl))
		return [0] * (self.__size - len(nl)) + nl

	def fake_move(self, d):
		if d == Board.LEFT or d == Board.RIGHT:
			chg, get = self.setLine, self.getLine
		elif d == Board.UP or d == Board.DOWN:
			chg, get = self.setCol, self.getCol

		new_cells = []
		for i in self.__size_range:
			origin = get(i)
			line = self.__moveLineOrCol(origin, d)
			collapsed, pts = self.__collapseLineOrCol(line, d)
			new = self.__moveLineOrCol(collapsed, d)
			new_cells += new

		return new_cells


	def move(self, d):
		if d == Board.LEFT or d == Board.RIGHT:
			chg, get = self.setLine, self.getLine
		elif d == Board.UP or d == Board.DOWN:
			chg, get = self.setCol, self.getCol
		else:
			return 0

		moved = False
		score = 0

		for i in self.__size_range:
			origin = get(i)
			line = self.__moveLineOrCol(origin, d)
			collapsed, pts = self.__collapseLineOrCol(line, d)
			new = self.__moveLineOrCol(collapsed, d)
			chg(i, new)
			if origin != new:
				moved = True
			score += pts

		if moved:
			self.addTile()

		return score