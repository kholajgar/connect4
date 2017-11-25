import numpy as np
from . import Board


def random_heur():
    return 1000 * (np.random.random() - 0.5)


class Node:
    def __init__(self, arr, debug=False, blist=None):
        self.brd = Board(arr=arr)
        self.debug = debug
        self.sequence = []
        if not blist:
            self.bias_list = self.gen_bias_list()
        else:
            self.bias_list = blist

    def find_best_col2play(self, depth2go, col_played):
        if depth2go == 0:
            best_val = hash(tuple(self.brd.get_array().flatten()))
            best_col = col_played
        else:
            best_col = -1
            c2p = self.brd.get_coin2play()
            best_val = -1 * c2p * np.Inf
            for col in self.bias_list:
                if self.add_in(col):
                    retcol, retval = self.find_best_col2play(
                        depth2go - 1, col)
                    if c2p * best_val < c2p * retval:
                        best_col, best_val = retcol, retval
                    self.remove_from(col)
        if self.debug:
            line2print = (
                "depth2go: {}, best_val: {}".format(
                    depth2go, best_val))
            print(line2print)
            input()
        return best_col, best_val

    def find_best_col2play_hash(self, depth2go, col_played):
        if depth2go == 0:
            best_val = random_heur()
            best_col = col_played
        else:
            best_col = -1
            c2p = self.brd.get_coin2play()
            best_val = -1 * c2p * np.Inf
            for col in self.bias_list:
                if self.add_in(col):
                    retcol, retval = self.find_best_col2play(
                        depth2go - 1, col)
                    if c2p * best_val < c2p * retval:
                        best_col, best_val = retcol, retval
                    self.remove_from(col)
        if self.debug:
            line2print = (
                "depth2go: {}, best_val: {}".format(
                    depth2go, best_val))
            print(line2print)
            input()
        return best_col, best_val

    def find_best_col2play_ab(
            self, depth2go, col_played,
            alpha=-np.Inf, beta=np.Inf):
        if depth2go == 0 or self.is_leaf():
            best_val = hash(tuple(self.brd.get_array().flatten()))
            best_col = col_played
        else:
            best_col = -1
            c2p = self.brd.get_coin2play()
            best_val = -1 * c2p * np.Inf
            for col in self.bias_list:
                if self.add_in(col):
                    retcol, retval = self.find_best_col2play_ab(
                        depth2go - 1, col, alpha, beta)
                    if c2p * best_val < c2p * retval:
                        best_col, best_val = retcol, retval

                    if c2p == 1:
                        alpha = max(alpha, best_val)
                    elif c2p == -1:
                        beta = min(beta, best_val)
                    self.remove_from(col)
                    if alpha >= beta:
                        break

        if self.debug:
            line2print = (
                "depth2go: {}, best_val: {}".format(
                    depth2go, best_val))
            print(line2print)
            input()
        return best_col, best_val

    def gen_bias_list(self):
        no_of_cols = self.brd.number_of_columns
        bias_list = [no_of_cols // 2]
        for i in range(1, no_of_cols // 2 + 1):
            bias_list.append(no_of_cols // 2 - i)
            bias_list.append(no_of_cols // 2 + i)
        if not no_of_cols % 2:
            bias_list = bias_list[:-1]
        return bias_list

    def add_in(self, col):
        bool2ret = self.brd.add_in(col)
        if self.debug:
            self.sequence.append(self.brd.get_coin2play()*-col)
            print(self.sequence)
            print(self.brd.get_array())
        return bool2ret

    def remove_from(self, col):
        self.brd.remove_from(col)
        if self.debug:
            del self.sequence[-1]
            print(self.sequence)
            print(self.brd.get_array())

    def is_leaf(self):
        return self.brd.is_board_full()
