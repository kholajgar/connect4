import matplotlib.pyplot as plt
import numpy as np
import itertools


class Board:
    def __init__(self, arr=None, win_len=4):

        if arr is None:
            self._board_array = np.zeros((6, 7), dtype=np.int32)
        else:
            self._board_array = arr

        self._win_len = win_len

        self._dtype = self._board_array.dtype
        self.number_of_rows = self._board_array.shape[0]
        self.number_of_columns = self._board_array.shape[1]

        self._area = 750

    def show_board(self):
        fig, ax = plt.subplots()
        ax.set_facecolor("xkcd:dark yellow")

        for row_number in range(self.number_of_rows):
            for col_number in range(self.number_of_columns):
                color = "white"
                if self._board_array[row_number, col_number] < -0.5:
                    color = "blue"
                elif self._board_array[row_number, col_number] > 0.5:
                    color = "red"
                # The step "self.number_of_rows - row_number - 1" below
                # ensures that the way the board is displayed
                # is aligned with the printed numpy array.
                ax.scatter(col_number,
                           self.number_of_rows - row_number - 1,
                           s=self._area, c=color)

        # the following gets rid of ticks
        for tic in ax.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
        for tic in ax.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False

        # this avoids auto-sizing
        ax.set_xlim([-0.75, self.number_of_columns - 0.25])
        ax.set_ylim([-0.75, self.number_of_rows - 0.25])
        ax.set_aspect("equal")

        return fig, ax

    def copy_arr2board(self, arr):
        """"Copies a given numpy array to self._board_array."""

        # Sanity check 1
        assert arr.shape == (self.number_of_rows,
                             self.number_of_columns)

        # Sanity check 2
        assert arr.dtype == self._dtype

        self._board_array = arr

    def get_array(self):
        return np.copy(self._board_array)

    def get_coin2play(self):
        if np.sum(self._board_array) == 0:
            coin2play = 1
        elif np.sum(self._board_array) == 1:
            coin2play = -1
        else:
            raise ValueError("The sum of the numpy array that is "
                             "representing the board, should be"
                             " either '0' or '1'.")
        return coin2play

    def getrow_givencol(self, col_number):
        """
        Given the column number returns (row
        the coin will land in) + 1. Returns 0 if the column
        is full of coins. Gravity is implemented here.
        """
        # noinspection PyUnresolvedReferences
        nonzeros = np.nonzero(self._board_array[:, col_number])[0]
        # import pdb
        # pdb.set_trace()
        if not len(nonzeros):
            return self.number_of_rows
        else:
            return np.min(nonzeros)

    def add_in(self, col_number):
        """Places the coin in the given column."""

        if not 0 <= col_number < self.number_of_columns:
            raise ValueError("Column number out of board!")

        row_number = self.getrow_givencol(col_number) - 1
        if row_number < 0:
            return False
        else:
            coin2play = self.get_coin2play()
            self._board_array[row_number, col_number] = coin2play
            return True

    def remove_from(self, col_number):
        """Removes the coin from the given column."""

        if not 0 <= col_number < self.number_of_columns:
            raise ValueError("Column number out of board!")

        row_number = self.getrow_givencol(col_number)
        if row_number >= self.number_of_rows:
            raise ValueError(
                "Trying to remove coin from an empty column!")
        else:
            self._board_array[row_number, col_number] = 0

    def is_board_full(self):
        arr1, arr2 = np.where(self._board_array == 0)

        # sanity check
        assert arr1.shape[0] == arr2.shape[0]

        if arr1.shape[0] == 0:
            return True
        else:
            return False

    def advi_diags(self):
        return [self._board_array[::-1, :].diagonal(i)
                for i in range(-self._board_array.shape[0] + 1,
                               self._board_array.shape[1])]

    def tidvi_diags(self):
        return [self._board_array.diagonal(i)
                for i in range(-self._board_array.shape[0] + 1,
                               self._board_array.shape[1])]

    def _get_max_length_dict(self):
        dict2ret = {}
        for rnum in range(self._board_array.shape[0]):
            local_vector = self._board_array[rnum, :]
            self._max_seq_length(dict2ret, local_vector)
        for cnum in range(self._board_array.shape[1]):
            local_vector = self._board_array[:, cnum]
            self._max_seq_length(dict2ret, local_vector)
        for local_vector in self.advi_diags():
            self._max_seq_length(dict2ret, local_vector)
        for local_vector in self.tidvi_diags():
            self._max_seq_length(dict2ret, local_vector)
        return dict2ret

    @staticmethod
    def _max_seq_length(dict2ret, local_vector):
        """This is a helper function."""
        for x in itertools.groupby(local_vector):
            my_key = x[0]
            my_list = list(x[1])
            if ((my_key not in dict2ret)
                    or (len(my_list) > dict2ret[my_key])):
                dict2ret[my_key] = len(my_list)

    def is_game_over(self):
        max_seq_dict = self._get_max_length_dict()
        winner = ""
        if max_seq_dict[-1] >= self._win_len:
            winner = "min"
        elif max_seq_dict[1] >= self._win_len:
            winner = "max"
        elif self.is_board_full():
            winner = "draw"
        return winner
