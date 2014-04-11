from numpy import zeros, array, nonzero, transpose, diff, where, delete
from random import choice

UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
GOAL = 11
SIZE = 4

HORIZONTAL, VERTICAL = 0, 1

class Board(object):
	def __init__(self, **kws):
		self.won = False
		self.cells = zeros((SIZE, SIZE))
		self.add_tile()
		self.add_tile()

	def can_move(self):
		return not self.filled() or (diff(self.cells) == 0).any() or (diff(self.cells, axis=0) == 0).any()

	def filled(self):
		return self.get_empty_cells().size == 0

	def add_tile(self):
		v = choice([1]*9+[2])
		empty = self.get_empty_cells()

		if empty.size != 0:
			x, y = choice(empty)
			self.cells[x][y] = v

	def getLine(self, y):
		return [self.cells[x][y] for x in range(SIZE)]

	def getCol(self, x):
		return [self.cells[x][y] for y in range(SIZE)]

	def setLine(self, y, l):
		for x in range(SIZE):
			self.cells[x][y] = l[x]

	def setCol(self, x, l):
		for y in range(SIZE):
			self.cells[x][y] = l[y]

	def get_empty_cells(self):
		return transpose((self.cells == 0).nonzero())

	def __collapseLineOrCol(self, line, d):
		if (d == LEFT or d == UP):
			inc = 1
			rg = range(0, SIZE - 1, inc)
		else:
			inc = -1
			rg = range(SIZE - 1, 0, inc)

		pts = 0
		for i in rg:
			if line[i] == 0:
				continue
			if line[i] == line[i+inc]:
				v = line[i]+1
				if v == GOAL:
					self.__won = True

				line[i] = v
				line[i+inc] = 0
				pts += 2 ** v

		return (line, pts)

	def __moveLineOrCol(self, line, d):
		nl = [c for c in line if c != 0]
		if d == UP or d == LEFT:
			return nl + [0] * (SIZE - len(nl))
		return [0] * (SIZE - len(nl)) + nl

	def fake_move(self, d):
		if d == LEFT or d == RIGHT:
			get, chunk = self.getLine, HORIZONTAL
		elif d == UP or d == DOWN:
			get, chunk = self.getCol, VERTICAL

		new_cells = []
		for i in range(SIZE):
			origin = get(i)
			line = self.__moveLineOrCol(origin, d)
			collapsed, pts = self.__collapseLineOrCol(line, d)
			new = self.__moveLineOrCol(collapsed, d)
			new_cells += new

		return self.chunk_board(new_cells, chunk)

	def chunk_board(self, cells, direction):
		return [cells[x :: SIZE] for x in range(SIZE)] if direction == VERTICAL else [cells[x * SIZE : (x + 1) * SIZE] for x in range(SIZE)]

	def move(self, d):
		if d == LEFT or d == RIGHT:
			chg, get = self.setLine, self.getLine
		elif d == UP or d == DOWN:
			chg, get = self.setCol, self.getCol
		else:
			return 0

		moved = False
		score = 0

		for i in range(SIZE):
			origin = get(i)
			line = self.__moveLineOrCol(origin, d)
			collapsed, pts = self.__collapseLineOrCol(line, d)
			new = self.__moveLineOrCol(collapsed, d)
			chg(i, new)
			if (array(origin) != array(new)).any():
				moved = True
			score += pts

		if moved:
			self.add_tile()

		return score