import numpy as np
from evyatar.Node import Node
from evyatar.EightPuzzle import reconstruct_solution
import random as rnd

goal_state = np.array([[1, 2, 3],
                       [0, 4, 6],
                       [7, 8, 5]])


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
    # todo: build h function with Manhattan distance
    pass


# Debug
a = np.array([[1, 2, 3],
              [0, 4, 6],
              [7, 8, 5]])

b = np.array([[1, 2, 3],
              [99, 4, 6],
              [7, 8, 5]])

c = np.array([[1, 2, 3],
              [999, 4, 6],
              [7, 8, 5]])

a_node = Node(a, 0, None)
b_node = Node(b, 0, a_node)
c_node = Node(c, 0, b_node)
sol = (reconstruct_solution(c_node))

