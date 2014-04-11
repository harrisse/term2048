from term2048.board import Board

from os import system

class Game(object):
	def __init__(self, next_move, hidemode=False, **kws):
		self.board = Board(**kws)
		self.score = 0
		self.next_move = next_move
		self.hidemode = hidemode

	def loop(self):
		while True:
			if not self.hidemode:
				system('cls')
				print self.__str__()
			if self.board.won() or not self.board.canMove():
				break
			m = self.next_move()
			self.score += self.board.move(m)

		return self.board.won(), self.score

	def __str__(self):
		b = self.board
		rg = range(b.size())
		s = '\n'.join([' ' * 4 + ' '.join(['%3d' % self.board.getCell(x, y) for x in rg]) for y in rg])

		top = '\n'*4
		bottom = '\n'*4
		scores = ' \tScore: %5d\n' % self.score
		return top + s.replace('\n', scores, 1) + bottom