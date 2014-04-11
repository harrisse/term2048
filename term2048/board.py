import random

UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

class Board(object):
	HORIZONTAL, VERTICAL = 0, 1

	GOAL = 11
	SIZE = 4

	def __init__(self, goal=GOAL, size=SIZE, **kws):
		self.__size = size
		self.__size_range = range(self.__size)
		self.__goal = goal
		self.__won = False
		self.cells = [[0]*self.__size for _ in range(self.__size)]
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

	def addTile(self, value=None, choices=([1]*9+[2])):
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
		for i in range(self.__size):
			self.setCell(x, i, l[i])

	def getEmptyCells(self):
		return [(x, y)
				for x in self.__size_range
				for y in self.__size_range if self.getCell(x, y) == 0]

	def __collapseLineOrCol(self, line, d):
		if (d == LEFT or d == UP):
			inc = 1
			rg = range(self.__size-1, inc)
		else:
			inc = -1
			rg = range(self.__size-1, 0, inc)

		pts = 0
		for i in rg:
			if line[i] == 0:
				continue
			if line[i] == line[i+inc]:
				v = line[i]+1
				if v == self.__goal:
					self.__won = True

				line[i] = v
				line[i+inc] = 0
				pts += 2 ** v

		return (line, pts)

	def __moveLineOrCol(self, line, d):
		nl = [c for c in line if c != 0]
		if d == UP or d == LEFT:
			return nl + [0] * (self.__size - len(nl))
		return [0] * (self.__size - len(nl)) + nl

	def fake_move(self, d):
		if d == LEFT or d == RIGHT:
			get, chunk = self.getLine, self.HORIZONTAL
		elif d == UP or d == DOWN:
			get, chunk = self.getCol, self.VERTICAL

		new_cells = []
		for i in self.__size_range:
			origin = get(i)
			line = self.__moveLineOrCol(origin, d)
			collapsed, pts = self.__collapseLineOrCol(line, d)
			new = self.__moveLineOrCol(collapsed, d)
			new_cells += new

		return self.chunk_board(new_cells, chunk)

	def chunk_board(self, cells, direction):
		return [cells[x :: self.__size] for x in range(self.__size)] if direction == self.VERTICAL else [cells[x * self.__size : (x + 1) * self.__size] for x in range(self.__size)]

	def move(self, d):
		if d == LEFT or d == RIGHT:
			chg, get = self.setLine, self.getLine
		elif d == UP or d == DOWN:
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