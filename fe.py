import sys
import os
import argparse
import time

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

    def print_board(self, board, one_color=None):
        os.system('clear')

        if one_color is None:
            for row in board:
                line = ["{0}  {1}".format(COLORS_MAP[j], CEND) for j in row]
                for cell in line:
                    print(cell, end='')
                print()
        else:
            for row in board:
                line = ["{0}  {1}".format(one_color, CEND) for j in row]
                for cell in line:
                    print(cell, end='')
                print()

    def game_over(self, board, msg):
        for _, c in COLORS_MAP.items():
            self.print_board(board, one_color=c)
            self.print_msg(msg)
            time.sleep(0.5)

    def get_conf(self):
        parser = argparse.ArgumentParser(description='Color Flood Game Configuration')
        parser.add_argument('-m', type=int, help='Number of rows in the board', required=False, default=18)
        parser.add_argument('-n', type=int, help='Number of columns in the board', required=False,  default=18)
        parser.add_argument('-w', '--win-turns', type=int, help='Maximum number of turns to win', required=False,  default=21)
        parser.add_argument('-c', '--colors', type=list, help='Game colors', required=False,  default=['r', 'b', 'g', 'y'])
        parser.add_argument('-j', '--jokers', type=int, help='Number of joker cells', required=False,  default=0)

        args = vars(parser.parse_args())

        return args

