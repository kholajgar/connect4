import matplotlib.pyplot as plt
import numpy as np
import itertools
from .board import Board


#-1 = blue. 1 = red. Engine is Blue for now. thus - Treat min as +10. 

class Engine:
    def __init__(self, arr=np.zeros((6, 7), dtype=np.int32), depth=3):

        self._dtype = arr.dtype
        self._board = Board(arr)    # maintaining own copy of board, to avoid searching on game board
        self._board.copy_arr2board(np.zeros((arr.shape),arr.dtype))    # have to refine this. in case of default arr not specified, problems due to Python using persistent array.
        self._board_array = arr
        self._number_of_rows = arr.shape[0]
        self._number_of_columns = arr.shape[1]
        self._depth = depth
    	
#    # Temporary Play_move :- makes Search of depth 1 and returns win if present else a valid move
#    def play_move(self, arr):
#        """ traverses the search tree and returns Column Number
#        Args:
#            arr :- present state of board
#        Returns:
#            int :- Column Number
#        """
#        self._board.copy_arr2board(arr)
#        for i in range(0,7):
#            move_result = self._board.insert_piece(i)
#            if move_result < 0:
#                continue
#            board_state = self._board.is_game_over() 
#            self._board.undo_move(move_result,i)
#            if board_state == "max":
#                continue
#            if board_state == "min":
#                return i
#            valid_move = i    
#        return valid_move  # Temporary


    # Temporary Play_move :- makes Search of depth 1 and returns win if present else a valid move
    def play_move(self, arr):
        """ traverses the search tree and returns Column Number
        Args:
            arr :- present state of board
        Returns:
            int :- Column Number
        """
        self._board.copy_arr2board(arr)
        best_move = 0
        best_val = -20
        for i in range(0,7):
            v = self.minimax(i, 1, True)
            if v > best_val:
                best_move = i
                best_val  = v
        return best_move

   
    def minimax(self, move, depth, maximizing_player):
        cur_color = "blue" if maximizing_player else "red"
        move_result = self._board.insert_piece(cur_color,move)
        heuristic_value = self.trivial_heuristic(maximizing_player)  #deciding whether terminal node based on heuristic. in actual - it will be based on a cheaper heuristic. (currently only have cheap)
        print("move" + str(move))
        print("depth" + str(depth))
        print("color" + cur_color)
        if heuristic_value != 0 or depth == 0 :
            self._board.undo_move(move_result,move)
            print("returning heuristic_val" + str(heuristic_value))
            return heuristic_value
        if maximizing_player:
            best_value = -20
            for i in range(0,7) :    #moves list/child list
                v = self.minimax(i, depth - 1, False)
                best_value = max(best_value, v)
            self._board.undo_move(move_result,move)
            print("returning best_val" + str(best_value))
            return best_value

        else:
            best_value = 20
            for i in range(0,7):
                v = self.minimax(i, depth - 1, True)
                best_value = min(best_value, v)
            self._board.undo_move(move_result,move)
            print("returning best_val" + str(best_value))
            return best_value

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
#        if not maximizing_player:
#            ret_value *= -1
        return ret_value
      								
