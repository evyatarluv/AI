import numpy as np
import copy


class Node:

    def __init__(self, table, g_value, lb, parent):

        self.table = table

        self.g_value = g_value

        self.lb = lb

        self.parent = copy.copy(parent)

    def expand(self):

        children = []
        empty_cell = np.where(self.table == 0)
        row, col = empty_cell[0][0], empty_cell[1][0]

        # Up
        try:
            children.append(swap(self.table, (row - 1, col), (row, col)))
        except IndexError:
            pass

        # Down
        try:
            children.append(swap(self.table, (row + 1, col), (row, col)))
        except IndexError:
            pass

        # Left
        try:
            children.append(swap(self.table, (row, col - 1), (row, col)))
        except IndexError:
            pass

        # Right
        try:
            children.append(swap(self.table, (row, col + 1), (row, col)))
        except IndexError:
            pass

        return children

    def depth(self):

        depth = 1
        p = self.parent

        while p is not None:
            depth += 1
            p = p.parent

        return depth

    def __eq__(self, other):

        if isinstance(other, Node):
            return (self.table == other.table).all()

        if isinstance(other, np.ndarray):
            return (self.table == other).all()

        return False

    def __str__(self):

        res = ''
        for i in range(len(self.table)):
            res += '|' + '|'.join(map(str, self.table[i])) + '| \n'

        return res


def swap(table, pos_1, pos_2):
    """
    This function swap between two elements in ndarray
    :param table:
    :param pos_1: position of the 1st element
    :param pos_2: position of the 2nd element
    :return:
    """
    # Dont use minus index (python can use it)
    if -1 in (pos_1 + pos_2):
        raise IndexError

    # Copy the table
    table = copy.deepcopy(table)

    # Swap
    temp = table[pos_1[0]][pos_1[1]]
    table[pos_1[0]][pos_1[1]] = table[pos_2[0]][pos_2[1]]
    table[pos_2[0]][pos_2[1]] = temp

    return table
