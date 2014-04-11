from term2048.ai import AI

from argparse import ArgumentParser

def parse_cli_args():
	parser = ArgumentParser(description='2048 in your terminal')
	parser.add_argument('--heur', dest='heuristic', type=str, default='player', help='heuristic to evaluate moves with')
	parser.add_argument('--hide', dest='hidemode', action='store_true', help='hide the ui')
	parser.add_argument('--iter', dest='iterations', type=int, default=1, help='iterations to play')
	parser.add_argument('--print', dest='print_interval', type=int, default=1, help='print every n iterations')
	parser.add_argument('--delay', dest='delay', type=float, default=0, help='adds artificial delay between moves')
	return vars(parser.parse_args())

def start_game():
	args = parse_cli_args()

	AI(**args)