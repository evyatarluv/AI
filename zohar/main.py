import numpy as np
from evyatar.Node import Node
from evyatar.EightPuzzle import EightPuzzle
import random as rnd

goal_state = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]])


def init_table(seed=None):
    """
    This function create initial state of the 8-table.
    he function return only solvable init table.
    :param seed: seed to the random function, optional
    :return:
    """

    if seed is not None:
        rnd.seed(seed)

    table = np.array(rnd.sample(range(9), 9)).reshape((3, 3))

    while not EightPuzzle.is_solvable(table):

        table = np.array(rnd.sample(range(9), 9)).reshape((3, 3))

    return table


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


def h_misplaced(table, goal_table):
    """
    h function which count the number of misplaced number in a given state
    :param table: current state, ndarray
    :param goal_table: goal state, ndarray
    :return: number of misplaced, int
    """

    # Flat both tables and change to list
    goal_table = list(goal_table.flatten())
    table = list(table.flatten())

    misplaced = 0

    for i in range(1, 9):
        # if the i number is misplaced
        if goal_table.index(i) != table.index(i):
            misplaced += 1

    return misplaced


def main():

    init_state = init_table()

    p = EightPuzzle(init_state, goal_state)

    sol = p.solve('BnB', h_manhattan)

    # Print solution
    for i in sol:
        print(i)
    print('\n\nSolution: {}'.format(len(sol) - 1))


if __name__ == '__main__':
    main()
    # pass

# Debug
a = np.array([[5, 0, 8],
              [4, 2, 1],
              [7, 3, 6]])

b = np.array([[1, 2, 3],
              [0, 4, 6],
              [7, 8, 5]])

a_node = Node(a, 0, None)
b_node = Node(b, 0, None)
h_manhattan(a, goal_state)
