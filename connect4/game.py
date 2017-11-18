import matplotlib.pyplot as plt
import numpy as np
import itertools
from .board import Board
from .engine import Engine

class Game:
    def __init__(self):
        self._board = Board()  # Currently creating default array of 6x7   
        print("Created New Game")
        #self._engine = Engine()

    def play(self, show_board=True):
        current_play = "red"
        while True:
            print("Enter move for "+current_play)
            while True:
                col_number = int(input())
                move_result = self._board.insert_piece(current_play, col_number)
                if move_result > 0:
                    break
                if move_result == -2:
                    print("Column Full. Play again ")
                else:
                    print("Invalid Column Number. Play again")
            is_game_over_result = self._board.is_game_over()
            if show_board:
                self._board.show_board()
                plt.show()
            if is_game_over_result:
                print("result is "+is_game_over_result)
                break
            current_play = "blue" if (current_play == "red") else "red"
    
    def new_game(self):
        arr = np.zeros((self._board.get_array().shape), dtype=self._board.get_array().dtype)
        self._board.copy_arr2board(arr)	
