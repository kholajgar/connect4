import matplotlib.pyplot as plt
import numpy as np
import itertools
from .board import Board
from random import shuffle
 

class Engine:
    def __init__(self, arr=None, depth=3):

        self._board = Board(arr)  # maintaining own copy of board, to avoid searching on game board
        if arr is None:
            self._board_array = np.zeros((6, 7), dtype=np.int32)
        else:
            self._board_array = arr
        self._number_of_rows = self._board_array.shape[0]
        self._number_of_columns = self._board_array.shape[1]
        self._dtype = self._board_array.dtype
        self._depth = depth

    def play_move(self, arr, depth):
        """ traverses the search tree and returns Column Number
        Args:
            arr :- present state of board
        Returns:
            int :- Column Number
        """
        self._board.copy_arr2board(arr)
        best_val, best_move = self.minimax(depth)
        return best_move

    def minimax(self, depth):
        """ traverses the search tree and returns Column Number
        Args:
            depth :- desired depth of minimax tree, at depth = 0, heuristic is computed
        Returns:
            tuple :- (best_value, best_move) 
        """
        
        c2p = self._board.get_coin2play()
        
        # deciding whether terminal node based on heuristic. in actual implementation
        # - it will be based on a cheaper heuristic. (currently only have cheap)
        heuristic_value = self.trivial_heuristic()
        best_move = -1
        if heuristic_value != 0 or depth == 0:
            return heuristic_value, best_move

        best_value = -1 * c2p * np.Inf
        col_list = list(range(self._number_of_columns))
        shuffle(col_list)
        for col in col_list:  # moves list/child list
            move_result = self._board.insert_piece_by_val(c2p, col)
            v, m = self.minimax(depth - 1)
            if c2p * best_value < c2p * v:
                best_value, best_move = v, col   
            self._board.undo_move(move_result, col)
        return best_value, best_move
 

    def trivial_heuristic(self):
        """ can only judge finished games
        Returns:
            int :- np.Inf if Max won, -np.Inf if Max lost, 0 otherwise
        """
        game_result = self._board.is_game_over()
        ret_value = 0
        if game_result == "max":
            ret_value = np.Inf
        if game_result == "min":
            ret_value = -np.Inf
        return ret_value
