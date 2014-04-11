from term2048.board import UP, DOWN, LEFT, RIGHT
from term2048.game import Game

from collections import Counter
from msvcrt import getch, kbhit
from random import choice
from os import system
from time import sleep, time

KEYS = {72: UP, 80: DOWN, 75: LEFT, 77: RIGHT}
DIRS = KEYS.values()

class AI:
	def player(self, board):
		while True:
			if kbhit() and ord(getch()) == 224:
				return KEYS[ord(getch())]

	def lookahead(self, board, heuristic, depth=0):
		scores = {direction: heuristic(self.mock_move(direction), depth - 1) for direction in DIRS}
		return choice(get_max_score(scores))

	def random(self, board):
		return 1

	def most_empty(self, board, depth=1):
		return Counter([x for row in board for x in row])[0] if depth == 0 else self.lookahead(board, self.most_empty, depth)
	
	def __init__(self, iterations=1, print_interval=1, delay=0, heuristic='most_empty', **kws):
		self.delay = delay
		self.heuristic = getattr(self, heuristic)
		total_won, total_score, start_time = 0, 0, time()

		for i in range(1, iterations):
			game = Game(self.get_move, **kws)
			self.board = game.board
			won, score = game.play()
			total_score += score
			total_won += won

			if i % print_interval == 0:
				system('cls')
				print 'iterations completed: ' + str(i)
				print 'simulations per second: ' + str(i / (time() - start_time))
				print 'average score: ' + str(total_score / i)
				print 'total won: ' + str(total_won)
				print 'proportion won: ' + str(total_won / i)

	def get_move(self):
		if self.delay != 0:
			sleep(self.delay)

		return self.heuristic(self.board)

	def mock_move(self, key):
		return self.board.fake_move(key)

def get_max_score(dictionary):
	inverse_dictionary = {v: [] for v in dictionary.values()}
	for (k, v) in dictionary.iteritems():
		inverse_dictionary[v].append(k)

	return inverse_dictionary[max(inverse_dictionary.keys())]