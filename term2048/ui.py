from __future__ import print_function
import sys
import argparse
from term2048.game import Game

def parse_cli_args():
	parser = argparse.ArgumentParser(description='2048 in your terminal')
	parser.add_argument('--mode', dest='mode', type=str, default=None, help='colors mode (dark or light)')
	parser.add_argument('--az', dest='azmode', action='store_true', help='use the letters a-z instead of numbers')
	parser.add_argument('--ai', dest='aimode', action='store_true', help='run with the ai')
	return vars(parser.parse_args())

def start_game():
	args = parse_cli_args()

	Game(**args).loop()