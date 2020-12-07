import numpy as np
import copy


class Node:

    def __init__(self, table, g_value, parent):

        self.table = table

        self.g_value = g_value

        if parent is None:
            self.parent = None
        else:
            self.parent = copy.deepcopy(parent)

    def expand(self):

        children = []
        empty_cell = np.where(self.table == 0)
        col, row = empty_cell[0][0], empty_cell[1][0]

        # Up
        try:
            children.append(swap(self.table, (row-1, col), (row, col)))
        except IndexError:
            pass

        # Down
        try:
            children.append(swap(self.table, (row+1, col), (row, col)))
        except IndexError:
            pass

        # Left
        try:
            children.append(swap(self.table, (row, col-1), (row, col)))
        except IndexError:
            pass

        # Right
        try:
            children.append(swap(self.table, (row, col+1), (row, col)))
        except IndexError:
            pass

        return children


def swap(table, pos_1, pos_2):
            """

            :param table:
            :param pos_1: position to move into the emtpy cell
            :param pos_2: position of the empty cell (0)
            :return:
            """

            table = table.copy()
            table[pos_2[0]][pos_2[1]] = table[pos_1[0]][pos_1[1]]
            table[pos_1[0]][pos_1[1]] = 0
            return table

