from term2048.board import Board, SIZE

from os import system

class Game(object):
	def __init__(self, next_move, hidemode=False, **kws):
		self.board = Board(**kws)
		self.score = 0
		self.next_move = next_move
		self.hidemode = hidemode

	def play(self):
		while True:
			if not self.hidemode:
				system('cls')
				print self.__str__()
			if self.board.won or not self.board.can_move():
				break
			self.score += self.board.move(self.next_move())

		return self.board.won, self.score

	def __str__(self):
		b = self.board
		rg = range(SIZE)
		s = '\n'.join(' '.join(str(cell) for cell in row) for row in self.board.cells)

		top = '\n' * 4
		bottom = '\n'*4
		scores = ' \tScore: %5d\n' % self.score
		return top + s.replace('\n', scores, 1) + bottom