import matplotlib.pyplot as plt
import numpy as np
import itertools



class Board:
    def __init__(self, arr=np.zeros((6, 7), dtype=np.int32), win_len=4):

        self._win_len = win_len

        self._dtype = arr.dtype
        self._board_array = arr
        self._number_of_rows = arr.shape[0]
        self._number_of_columns = arr.shape[1]

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

    def undo_move(self, row_number=0, col_number=0):
        self._board_array[row_number][col_number] = 0    

    def insert_piece(self, color="red", col_number=0):
        """insert piece with gravity
        Args:
            color ("string"): Color of piece to insert - "red" or "blue"
            col_number ("int"): Column Number to insert the column to
        Returns:
            int: The return value. -1 if invalid else row number where piece was inserted.
        """
        if col_number < 0 or col_number > self._number_of_columns:
            #print("Invalid Column Number")
            return -1
        empty_squares = (np.where(self._board_array.T[col_number] == 0))[0]
        if empty_squares.shape[0] == 0:
            #print("Column full")
            return -2
        self._board_array[empty_squares[-1]][col_number] = 1 if color == "red" else -1
        return empty_squares[-1]

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
        Given the column number returns which row
        the coin will land in. Returns -1 if the column
        is full of coins. Gravity is implemented here.
        """
        # start from the largest row number
        # (which is the bottom-most row)
        row_number = self._number_of_rows - 1
        while row_number >= 0:
            if self._board_array[
                    row_number, col_number] == 0:
                break
            else:
                row_number -= 1
        return row_number

    def play_in(self, col_number):
        """Places the coin in the given column."""

        if not 0 <= col_number < self._number_of_columns:
            raise ValueError("Column number out of board!")

        row_number = self.getrow_givencol(col_number)
        if row_number < 0:
            return False
        else:
            coin2play = self.get_coin2play()
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
        if -1 in max_seq_dict and max_seq_dict[-1] >= self._win_len:
            winner = "min"
        elif 1 in max_seq_dict and max_seq_dict[1] >= self._win_len:
            winner = "max"
        elif self.is_board_full():
            winner = "draw"
        return winner
