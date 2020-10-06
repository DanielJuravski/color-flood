import sys
import argparse

COLORS_MAP = {'r': '\033[41m', 'b': '\033[44m', 'g': '\033[42m', 'y': '\033[43m'}
CEND = '\033[0m'


class CLI:
    def __init__(self):
        pass

    def print_msg(self, msg=''):
        print(msg)

    def get_input(self, msg):
        user_input = input(msg)

        return user_input

    def print_board(self, board):
        for row in board:
            line = ["{0}  {1}".format(COLORS_MAP[j], CEND) for j in row]
            for cell in line:
                print(cell, end='')
            print()

    def get_conf(self):
        parser = argparse.ArgumentParser(description='Color Flood Game Configuration')
        parser.add_argument('-m', type=int, help='Number of rows in the board', required=False, default=18)
        parser.add_argument('-n', type=int, help='Number of columns in the board', required=False,  default=18)
        parser.add_argument('-w', '--win-turns', type=int, help='Maximum number of turns to win', required=False,  default=21)
        parser.add_argument('-c', '--colors', type=list, help='Game colors', required=False,  default=['r', 'b', 'g', 'y'])
        parser.add_argument('-j', '--jokers', type=int, help='Number of joker cells', required=False,  default=0)

        args = vars(parser.parse_args())

        return args

