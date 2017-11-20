import matplotlib.pyplot as plt
import numpy as np
import itertools
from .board import Board


# -1 = blue. 1 = red. Engine is Blue for now. thus - Treat "min" game state as +10.

class Engine:
    def __init__(self, arr=np.zeros((6, 7), dtype=np.int32), depth=3):

        self._dtype = arr.dtype
        self._board = Board(arr)  # maintaining own copy of board, to avoid searching on game board
        # have to refine this. in case of default arr not specified,
        # problems due to Python using persistent array.
        self._board.copy_arr2board(np.zeros((arr.shape),
                                            arr.dtype))
        self._board_array = arr
        self._number_of_rows = arr.shape[0]
        self._number_of_columns = arr.shape[1]
        self._depth = depth

    def play_move(self, arr):
        """ traverses the search tree and returns Column Number
        Args:
            arr :- present state of board
        Returns:
            int :- Column Number
        """
        self._board.copy_arr2board(arr)
        best_val, best_move = self.minimax(1, True)
        return best_move

    # currently has debug prints, will be removed.
    def minimax(self, depth, maximizing_player):
        """ traverses the search tree and returns Column Number
        Args:
            depth :- desired depth of minimax tree, at depth = 0, heuristic is computed
            maximizing_player :- boolean - when true, will return score of maximizing player
        Returns:
            tuple :- (best_value, best_move) 
        """
        cur_color = "blue" if maximizing_player else "red"
        # deciding whether terminal node based on heuristic. in actual implementation
        # - it will be based on a cheaper heuristic. (currently only have cheap)
        heuristic_value = self.trivial_heuristic(maximizing_player)
        # print("depth " + str(depth))
        # print("color " + cur_color)
        best_move = -1
        if heuristic_value != 0 or depth == 0:
            # print("returning heuristic_val  " + str(heuristic_value))
            # print("returning best_move " + str(best_move))
            # print("***********************")
            return heuristic_value, best_move
        if maximizing_player:
            best_value = -20
            for i in range(0, 7):  # moves list/child list
                move_result = self._board.insert_piece(cur_color, i)
                v, m = self.minimax(depth - 1, False)
                best_value = max(best_value, v)
                if best_value == v:
                    best_move = i
                self._board.undo_move(move_result, i)
            # print("returning best_val " + str(best_value))
            # print("returning best_move " + str(best_move))
            # print("***********************")
            return best_value, best_move

        else:
            best_value = 20
            for i in range(0, 7):
                move_result = self._board.insert_piece(cur_color, i)
                v, m = self.minimax(depth - 1, True)
                best_value = min(best_value, v)
                if best_value == v:
                    best_move = i
                self._board.undo_move(move_result, i)
            # print("returning best_val " + str(best_value))
            # print("returning best_move " + str(best_move))
            # print("***********************")
            return best_value, best_move

    def trivial_heuristic(self, maximizing_player):
        """ can only judge finished games
        Returns:
            int :- +10 if won, -10 if lost, 0 otherwise
        """
        game_result = self._board.is_game_over()
        ret_value = 0
        if game_result == "max":
            ret_value = -10
        if game_result == "min":
            ret_value = 10
        return ret_value
