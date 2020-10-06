import numpy as np
from copy import deepcopy

M = 18
N = 18
COLORS = ['r', 'b', 'g', 'y']
COLORS_MAP = {'r': '\033[41m', 'b': '\033[44m', 'g': '\033[42m', 'y': '\033[43m'}
CEND = '\033[0m'
WIN_TURNS = 21


class Game:
    """
    color flood game
    """
    def __init__(self):
        """
        init game - supporting actions history and knight mode
        """
        self.board_history = []
        self.board = self.init_board()
        self.board_history.append(deepcopy(self.board))
        self.possible_directions = [(-1, 0), (0, +1), (+1, 0), (0, -1)]
        self.knight_directions = [(-2, +1), (-1, +2), (+1, +2), (+2, +1), (+2, -1), (+1, -2), (-1, -2), (-2, -1)]
        self.knight_mode = False

    def init_board(self):
        """
        create M*N board randomly values with the COLORS chars
        :return:
        """
        print("Initializing board at size {}*{}".format(M, N))
        board = np.random.choice(COLORS, size=(M, N))
        print()

        return board

    def play(self):
        """
        play loop until all the board is one color
        :return:
        """
        turn_current = 0
        self.print_board()

        # play until the game is end
        while not self.is_game_end():
            user_input = self.get_user_input(turn_current)

            if user_input == 'u':
                # undo last move (last color spreading)
                if len(self.board_history) > 1:
                    self.board_history.pop()
                    self.board = deepcopy(self.board_history[-1])
                    turn_current -= 1
            elif user_input == 'k':
                # set knight mode - the alg. for color spreading is calculated via the knight steps
                self.knight_mode = not self.knight_mode
            else:
                # spread colors to all the neighbors
                self.spread_colors(user_input)
                turn_current += 1
                self.board_history.append(deepcopy(self.board))

            self.print_board()

        self.game_end(turn_current)

    def is_game_end(self):
        """
        check all matrix values are the same color
        :return:
        """
        eq = np.all(self.board == self.board[0][0])

        return eq

    def game_end(self, turn_current):
        if turn_current <= WIN_TURNS:
            print("Game Over, You Win!")
        else:
            print("Game Over, You Lose!")

    def get_user_input(self, turn_current):
        """
        get char input from user, supports only COLORS values, u value - for undo, k value for knight mode
        :param turn_current:
        :return:
        """
        is_input_valid = False
        while not is_input_valid:
            if self.knight_mode:
                input_msg = "{0}/{1} Moves (knight mode). Insert color:".format(turn_current, WIN_TURNS)
            else:
                input_msg = "{0}/{1} Moves. Insert color:".format(turn_current, WIN_TURNS)
            user_input = input(input_msg)
            if user_input in COLORS or user_input == 'u' or user_input == 'k':
                is_input_valid = True
                print()

        return user_input

    def print_board(self):
        for row in self.board:
            line = ["{0}  {1}".format(COLORS_MAP[j], CEND) for j in row]
            for cell in line:
                print(cell, end='')
            print()

    def spread_colors(self, new_color):
        """
        spread color to all the 0,0 neighbors that had the previous color that 0,0 had
        :param new_color:
        :return:
        """
        cands_approved = set()
        cands_approved.add((0, 0))
        cands_declined = set()
        cells, _ = self.get_neighbors_to_color(0, 0, cands_approved, cands_declined)

        for (i, j) in cells:
            self.board[i][j] = new_color

    def get_neighbors_to_color(self, i, j, cands_approved, cands_declined):
        """
        find all neighbors of i,j cell (by the desired directions mode) that have the same color as it has
        :param i: src cell i value
        :param j: src cell j value
        :param cands_approved: cells that already were checked and approved as neighbors to be colored - shouldn't be checked again
        :param cands_declined: cells that already were checked and declined as neighbors to be colored - shouldn't be checked again
        :return: cands_approved, cands_declined
        """
        # set the desired directions to search on
        directions = self.possible_directions if self.knight_mode == False else self.knight_directions
        for cand_direction in directions:
            cand_i = i + cand_direction[0]
            cand_j = j + cand_direction[1]

            # if the cand cell in one of the bellow list - do not search it
            if (cand_i, cand_j) in cands_approved or (cand_i, cand_j) in cands_declined:
                continue

            # try to access some i,j in the board matrix
            try:
                # cand i,j can be negative due to some directions - ignore them
                if cand_i < 0 or cand_j < 0:
                    continue
                # check if cand cell color as the src cell color
                if self.board[cand_i][cand_j] == self.board[i][j]:
                    cands_approved.add((cand_i, cand_j))

                    # search all neighbors of the accepted neighbor
                    partial_cands_approved, partial_cands_declined = self.get_neighbors_to_color(cand_i, cand_j,
                                                                                                 cands_approved,
                                                                                                 cands_declined)
                    cands_approved.union(partial_cands_approved)
                    cands_declined.union(partial_cands_declined)
                else:
                    cands_declined.add((cand_i, cand_j))

            # that try should except on IndexError values
            except IndexError as e:
                continue

        return cands_approved, cands_declined


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
