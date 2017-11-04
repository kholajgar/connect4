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
                ax.scatter(col_number, row_number,
                           s=self._area, c="white")

        for tic in ax.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
        for tic in ax.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False

        return fig, ax
