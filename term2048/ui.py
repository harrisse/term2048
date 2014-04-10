import sys
import argparse
from term2048.game import Game
from term2048.ai import AI

def parse_cli_args():
	parser = argparse.ArgumentParser(description='2048 in your terminal')
	parser.add_argument('--ai', dest='aimode', action='store_true', help='run with the ai')
	parser.add_argument('--heur', dest='heuristic', type=str, default=0, help='heuristic to evaluate moves with')
	parser.add_argument('--hide', dest='hidemode', action='store_true', help='hide the ui')
	parser.add_argument('--iter', dest='iterations', type=int, default=1, help='iterations to play')
	parser.add_argument('--print', dest='print_interval', type=int, default=1, help='print every n iterations')
	parser.add_argument('--delay', dest='delay', type=float, default=0, help='adds artificial delay between moves')
	return vars(parser.parse_args())

def start_game():
	args = parse_cli_args()

	if args['aimode']:
		AI(**args)
	else:
		Game(**args).loop()