import numpy as np
from copy import deepcopy
from fe import CLI


class Game:
    """
    color flood game
    """
    def __init__(self):
        """
        init game - supporting actions history and knight mode
        """
        self.fe = CLI()
        self.conf = self.init_conf()
        self.board_history = []
        self.board = self.init_board()
        self.board_history.append(deepcopy(self.board))
        self.possible_directions = [(-1, 0), (0, +1), (+1, 0), (0, -1)]
        self.knight_directions = [(-2, +1), (-1, +2), (+1, +2), (+2, +1), (+2, -1), (+1, -2), (-1, -2), (-2, -1)]
        self.knight_mode = False
        self.joker_cells = self.init_jokers()

    def init_conf(self):
        conf = self.fe.get_conf()
        print(conf)

        return conf

    def init_board(self):
        """
        create M*N board randomly values with the COLORS chars
        :return:
        """
        m = self.conf['m']
        n = self.conf['n']

        msg = "Initializing board at size {}*{}\n".format(m, n)
        self.fe.print_msg(msg)
        board = np.random.choice(self.conf['colors'], size=(m, n))

        return board

    def init_jokers(self):
        """
        randomize jokers cells in the board
        :return:
        """
        cells = []
        for _ in range(self.conf['jokers']):
            joker_i = np.random.choice(self.conf['m'])
            joker_j = np.random.choice(self.conf['n'])

            cells.append((joker_i, joker_j))

        return cells

    def play(self):
        """
        play loop until all the board is one color
        :return:
        """
        turn_current = 0
        self.fe.print_board(self.board)

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
            elif user_input == 'q':
                self.fe.print_msg("Good Bye!")
                exit(0)
            else:
                # spread colors to all the neighbors
                self.spread_colors(user_input)
                turn_current += 1
                self.board_history.append(deepcopy(self.board))

            self.fe.print_board(self.board)

        self.game_end(turn_current)

    def is_game_end(self):
        """
        check all matrix values are the same color
        :return:
        """
        eq = np.all(self.board == self.board[0][0])

        return eq

    def game_end(self, turn_current):
        if turn_current <= self.conf['win_turns']:
            msg = "Game Over, You Win! (you made it with {}/{} moves)".format(turn_current, self.conf['win_turns'])
        else:
            msg = "Game Over, You Lose! (you made it with {}/{} moves)".format(turn_current, self.conf['win_turns'])
        self.fe.game_over(self.board, msg)

    def get_user_input(self, turn_current):
        """
        get char input from user, supports only COLORS values,
        u value - for undo,
        k value for knight mode,
        q value - exit the game
        :param turn_current:
        :return:
        """
        is_input_valid = False
        while not is_input_valid:
            if self.knight_mode:
                input_msg = "{0}/{1} Moves (knight mode). Insert color:".format(turn_current, self.conf['win_turns'])
            else:
                input_msg = "{0}/{1} Moves. Insert color:".format(turn_current, self.conf['win_turns'])
            user_input = self.fe.get_input(input_msg)
            if user_input in self.conf['colors'] or user_input == 'u' or user_input == 'k' or user_input == 'q':
                is_input_valid = True
                self.fe.print_msg()

        return user_input

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
            if (i, j) in self.joker_cells:
                neighbors = self.get_direct_neighbors(i, j)
                for (n_i, n_j) in neighbors:
                    self.board[n_i][n_j] = new_color
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

    def get_direct_neighbors(self, i, j):
        """
        get direct neighbors via 4 close neighbors
        :param i:
        :param j:
        :return:
        """
        neighbors = []
        for cand_direction in self.possible_directions:
            cand_i = i + cand_direction[0]
            cand_j = j + cand_direction[1]

            # try to access some i,j in the board matrix
            try:
                # cand i,j can be negative due to some directions - ignore them
                if cand_i < 0 or cand_j < 0:
                    continue
            # that try should except on IndexError values
            except IndexError as e:
                continue

            neighbors.append((cand_i, cand_j))

        return neighbors


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
