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
