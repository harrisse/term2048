from numpy import zeros, array, nonzero, transpose, diff, where, delete, int16, array_equal, copy, pad
from random import choice, random

UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
GOAL = 11
SIZE = 4

HORIZONTAL, VERTICAL = 0, 1

def collapse(board, d):
	has_changed = False

	for i in range(SIZE):
		row = board[i] if d == UP or d == DOWN else board[:, i]
		new_row = zeros(SIZE)
		new_vals = row[row.nonzero()]

		if len(new_vals) > 0:
			if (d == UP or d == LEFT):
				new_row[:len(new_vals)] = new_vals
			else:
				new_row[-len(new_vals):] = new_vals

		if not has_changed and not array_equal(row, new_row):
			has_changed = True

		if d == UP or d == DOWN:
			board[i] = new_row
		else:
			board[:, i] = new_row

	return has_changed

class Board(object):
	def __init__(self, **kws):
		self.won = False
		self.cells = zeros((SIZE, SIZE), dtype=int16)
		self.add_tile()
		self.add_tile()

	def can_move(self):
		return (self.cells == 0).any() or (diff(self.cells) == 0).any() or (diff(self.cells, axis=0) == 0).any()

	def add_tile(self):
		empty_cells = self.cells == 0

		if empty_cells.any():
			x, y = choice(transpose(empty_cells.nonzero()))
			self.cells[x][y] = 1 if random() < .9 else 2

	def get_col(self, x):
		return copy(self.cells[x])

	def get_row(self, x):
		return copy(self.cells[:, x])

	def set_row(self, x, l):
		self.cells[:, x] = l

	def set_col(self, y, l):
		self.cells[y] = l

	def __collapseLineOrCol(self, line, d):
		line = copy(line)
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
			get, chunk = self.get_row, HORIZONTAL
		elif d == UP or d == DOWN:
			get, chunk = self.get_col, VERTICAL

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
			chg, get = self.set_row, self.get_row
		elif d == UP or d == DOWN:
			chg, get = self.set_col, self.get_col
		else:
			return 0

		score = 0

		moved = collapse(self.cells, d)
		for i in range(SIZE):
			origin = get(i)
			new, pts = self.__collapseLineOrCol(origin, d)
			chg(i, new)
			if (not array_equal(origin, new)):
				moved = True
			score += pts
		moved2 = collapse(self.cells, d)

		if moved or moved2:
			self.add_tile()

		return score