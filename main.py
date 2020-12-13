import numpy as np
from Node import Node
from EightPuzzle import EightPuzzle
import random as rnd
from heuristic import *

goal_state = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]])


def main():

    init_state = EightPuzzle.init_table()

    puzzle = EightPuzzle(init_state, goal_state)

    sol = puzzle.solve('A*', h_manhattan)

    # Print solution
    for i in sol:
        print(i)
    print('\n\nSolution: {}'.format(len(sol) - 1))


if __name__ == '__main__':

    main()