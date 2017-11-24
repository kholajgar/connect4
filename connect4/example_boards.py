from .board import Board
import numpy as np


def get_example_boards():
    list2ret = []

    arr = np.array(
          [[0,  0,  0,  0,  0,  0,  0],
           [0,  1,  0,  0,  0,  0,  0],
           [0, -1, -1,  1,  0,  0,  0],
           [0,  1, -1, -1, -1, -1,  0],
           [0,  1,  1, -1, -1, -1,  1],
           [1,  1, -1,  1,  1,  1, -1]])
    brd = Board(arr)
    list2ret.append(brd)

    arr = np.array(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, -1, 0, 0, 0, 0],
         [-1, 1, 1, 1, 1, 0, 0],
         [-1, -1, 1, 1, 1, -1, -1]])
    brd = Board(arr)
    list2ret.append(brd)

    arr = np.array(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, -1, -1, 1, 0],
         [0, 0, 0, 1, 1, -1, 0],
         [-1, 0, 0, 1, -1, 1, 0],
         [-1, 0, 1, 1, -1, 1, 0]])
    brd = Board(arr)
    list2ret.append(brd)

    return list2ret
