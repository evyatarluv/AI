import numpy as np
from evyatar.Node import Node
from evyatar.EightPuzzle import reconstruct_solution
import random as rnd

goal_state = np.array([[1, 2, 3],
                       [0, 4, 6],
                       [7, 8, 5]])


def init_table(seed=None):

    if seed is not None:
        rnd.seed(seed)

    # todo: make it more clear!!!!!!
    numbers = range(9)
    rnd.shuffle(numbers)
    table = np.array(numbers).reshape((3, 3))

    return table


# todo: build h function with Manhattan distance

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

