import numpy as np
from evyatar.Node import Node
from evyatar.EightPuzzle import EightPuzzle
import random as rnd

goal_state = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]])


def init_table(seed=None):

    """
    This function create initial state of the 8-puzzle
    :param seed: seed to the random function, optional
    :return:
    """

    if seed is not None:
        rnd.seed(seed)

    return np.array(rnd.sample(range(9), 9)).reshape((3, 3))


def h_manhattan(table, goal_table):
    """
    This h function calculate the sum of manhattan distance between current table
    to the goal table.
    :param table: current table, ndarray with shape (3,3)
    :param goal_table: gaol state table, ndarray with shape (3,3)
    :return:
    """

    manhattan_sum = 0

    for i in range(1, 9):

        # Get position on current table
        table_pos = np.where(table == i)

        # Get position on goal table
        goal_pos = np.where(goal_table == i)

        # Compute manhattan distance and sum
        x_distance = np.abs(table_pos[0][0] - goal_pos[0][0])
        y_distance = np.abs(table_pos[1][0] - goal_pos[1][0])
        manhattan_sum += x_distance + y_distance

    return manhattan_sum


def main():

    init_state = init_table()

    p = EightPuzzle(init_state, goal_state)

    p.solve('BnB', h_manhattan)


if __name__ == '__main__':
    main()
# Debug
a = np.array([[1, 2, 3],
              [0, 4, 6],
              [7, 8, 5]])

b = np.array([[1, 2, 3],
              [0, 4, 6],
              [7, 8, 5]])

h_manhattan(a, goal_state)
