import sys
import numpy as np
from termcolor import colored
from sty import fg, bg, ef, rs
from copy import deepcopy


M = 18
N = 18
COLORS = ['r', 'b', 'g', 'y']
COLORS_MAP = {'r': '\033[41m', 'b': '\033[44m', 'g': '\033[42m', 'y': '\033[43m'}
CEND = '\033[0m'

WIN_TURNS = 21


class Game:
    def __init__(self):
        self.board_history = []
        self.board = self.init_board()
        self.board_history.append(deepcopy(self.board))
        self.possible_directions = [(-1, 0), (0, +1), (+1, 0), (0, -1)]

    def init_board(self):
        print("Initializing board at size {}*{}".format(M, N))
        board = np.random.choice(COLORS, size=(M, N))
        print()

        return board

    def play(self):
        turn_current = 0
        self.print_board()

        while not self.is_game_end():
            user_input = self.get_user_input(turn_current)

            if user_input == 'u':
                if len(self.board_history) > 1:
                    self.board_history.pop()
                    self.board = deepcopy(self.board_history[-1])
                    turn_current -= 1
            else:
                self.spread_colors(user_input)
                turn_current += 1
                self.board_history.append(deepcopy(self.board))

            self.print_board()

        self.game_end(turn_current)

    def is_game_end(self):
        eq = np.all(self.board == self.board[0][0])

        return eq

    def game_end(self, turn_current):
        if turn_current <= WIN_TURNS:
            print("Game Over, You Win!")
        else:
            print("Game Over, You Lose!")

    def get_user_input(self, turn_current):
        is_input_valid = False
        while not is_input_valid:
            user_input = input("{0}/{1} Moves. Insert color:".format(turn_current, WIN_TURNS))
            if user_input in COLORS or user_input == 'u':
                is_input_valid = True

        return user_input

    def print_board(self):
        for row in self.board:
            line = ["{0}  {1}".format(COLORS_MAP[j], CEND) for j in row]
            for cell in line:
                print(cell, end='')
            print()

    def spread_colors(self, new_color):
        cands_approved = set()
        cands_approved.add((0, 0))
        cands_declined = set()
        cells, _ = self.get_neighbors_to_color(0, 0, cands_approved, cands_declined)

        for (i, j) in cells:
            self.board[i][j] = new_color

    def get_neighbors_to_color(self, i, j, cands_approved, cands_declined):
        for cand_direction in self.possible_directions:
            cand_i = i + cand_direction[0]
            cand_j = j + cand_direction[1]

            if (cand_i, cand_j) in cands_approved or (cand_i, cand_j) in cands_declined:
                continue

            try:
                if cand_i < 0 or cand_j < 0:
                    continue
                if self.board[cand_i][cand_j] == self.board[i][j]:
                    cands_approved.add((cand_i, cand_j))

                    partial_cands_approved, partial_cands_declined = self.get_neighbors_to_color(cand_i, cand_j,
                                                                                                 cands_approved,
                                                                                                 cands_declined)
                    cands_approved.union(partial_cands_approved)
                    cands_declined.union(partial_cands_declined)
                else:
                    cands_declined.add((cand_i, cand_j))

            except IndexError as e:
                continue

        return cands_approved, cands_declined


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
