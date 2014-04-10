from term2048.board import Board
from term2048.game import Game
from time import sleep, time
from random import randrange, choice
from collections import Counter
from os import system

class AI:
	__keys = [
		Board.UP,
		Board.DOWN,
		Board.LEFT,
		Board.RIGHT,
	]
	
	def __init__(self, iterations=1, print_interval=1, delay=0, **kws):
		self.__delay = delay
		total_won, total_score = 0, 0
		start_time = time()
		for i in range(iterations):
			game = Game(ai=self, **kws)
			self.board = game.board
			won, score = game.loop()
			total_score = total_score + score
			if won:
				total_won = total_won + 1

			if i % print_interval == 0:
				system('cls')
				print 'iterations completed: ' + str(i)
				print 'simulations per second: ' + str(i / (time() - start_time))
				print 'average score: ' + str(total_score / (i + 1.0))
				print 'proportion won: ' + str(total_won / (i + 1.0))


	def getMove(self):
		if self.__delay != 0:
			sleep(self.__delay)
		
		boards = {key: self.board.fake_move(key) for key in self.__keys}
		flat_boards = {key: [x for row in boards[key] for x in row] for key in self.__keys}
		histograms = {key: Counter(flat_boards[key]) for key in self.__keys}
		open_cells = {key: histograms[key][0] for key in self.__keys}

		inv_map = {}
		for k, v in open_cells.iteritems():
			inv_map[v] = inv_map.get(v, [])
			inv_map[v].append(k)

		return choice(inv_map[max(inv_map.keys())])