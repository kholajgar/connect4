import matplotlib.pyplot as plt
import numpy as np


class Board:
    def __init__(self, number_of_rows=6, number_of_columns=7):
        self._dtype = np.int32
        self._board_array = np.zeros(
            (number_of_rows, number_of_columns),
            dtype=self._dtype)
        self._number_of_rows = number_of_rows
        self._number_of_columns = number_of_columns

        self._area = 750

    def show_board(self):
        fig, ax = plt.subplots()
        ax.set_facecolor("xkcd:dark yellow")

        for row_number in range(self._number_of_rows):
            for col_number in range(self._number_of_columns):
                color = "white"
                if self._board_array[row_number, col_number] < -0.5:
                    color = "blue"
                elif self._board_array[row_number, col_number] > 0.5:
                    color = "red"
                # The step "self._number_of_rows - row_number - 1" below
                # ensures that the way the board is displayed
                # is aligned with the printed numpy array.
                ax.scatter(col_number,
                           self._number_of_rows - row_number - 1,
                           s=self._area, c=color)

        # the following gets rid of ticks
        for tic in ax.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
        for tic in ax.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False

        # this avoids auto-sizing
        ax.set_xlim([-0.75, self._number_of_columns - 0.25])
        ax.set_ylim([-0.75, self._number_of_rows - 0.25])
        ax.set_aspect("equal")

        return fig, ax

    def copy_arr2board(self, arr):
        """"Copies a given numpy array to self._board_array."""

        # Sanity check 1
        assert arr.shape == (self._number_of_rows,
                             self._number_of_columns)

        # Sanity check 2
        assert arr.dtype == self._dtype

        self._board_array = arr

    def get_array(self):
        return np.copy(self._board_array)

    def play_in(self, col_number):
        """Places the coin in the given column."""

        if not 0 <= col_number < self._number_of_columns:
            raise ValueError("Column number out of board!")

        # start from the largest row number
        # (which is the bottom-most row)
        row_number = self._number_of_rows - 1
        while row_number >= 0:
            if self._board_array[
                    row_number, col_number] == 0:
                break
            else:
                row_number -= 1

        if row_number < 0:
            return "column_full"

        if np.sum(self._board_array) == 0:
            coin2play = 1
        elif np.sum(self._board_array) == 1:
            coin2play = -1
        else:
            raise ValueError("The sum of the numpy array that is "
                             "representing the board, should be"
                             " either '0' or '1'.")

        self._board_array[row_number, col_number] = coin2play

        return True

    def is_board_full(self):
        arr1, arr2 = np.where(self._board_array == 0)

        # sanity check
        assert arr1.shape[0] == arr2.shape[0]

        if arr1.shape[0] == 0:
            return True
        else:
            return False
