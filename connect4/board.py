import matplotlib.pyplot as plt
import numpy as np


class Board:
    def __init__(self, number_of_rows=6, number_of_columns=7):
        self.board_array = np.zeros((number_of_rows, number_of_columns))
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns

        self._area = np.pi * (15 * 1) ** 2

    def show_board(self):
        fig, ax = plt.subplots()
        ax.set_facecolor("xkcd:yellow")

        for row_number in range(self.number_of_rows):
            for col_number in range(self.number_of_columns):
                if self.board_array[row_number][col_number] == 0:
                    ax.scatter(col_number, row_number,
                               s=self._area, c="white")
                elif self.board_array[row_number][col_number] == 1:
                    ax.scatter(col_number, row_number,
                               s=self._area, c="blue")
                else:
                    ax.scatter(col_number, row_number,
                               s=self._area, c="red")

        for tic in ax.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
        for tic in ax.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False

        return fig, ax

    def insert_piece(self, color="red", col_number=0):
        """insert piece with gravity
        Args:
            color ("string"): Color of piece to insert - "red" or "blue"
            col_number ("int"): Column Number to insert the column to
        Returns:
            int: The return value. -1 if invalid else row number where piece was inserted.
        """
        if col_number < 0 or col_number > 6:
            print("Invalid Column Number")
            return -1
        empty_squares = (np.where(self.board_array.T[col_number] == 0))[0]
        if empty_squares.shape[0] == 0:
            print("Column full")
            return -1
        self.board_array[empty_squares[0]][col_number] = -1 if color == "red" else 1
        return empty_squares[0]

