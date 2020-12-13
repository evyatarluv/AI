import numpy as np
from EightPuzzle import EightPuzzle
import random as rnd
from heuristics import *
from time import time
from tqdm import tqdm

goal_state = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]])


def main():
    """
    The main function initialize a random (solvable) table and return a solution.
    :return:
    """

    # Init table
    init_state = EightPuzzle.init_table(seed=51)

    # Solve the init table
    puzzle = EightPuzzle(init_state, goal_state)

    solution = puzzle.solve('A*', h_misplaced)

    # Print solution
    print('Solution Way:')
    print(*solution, sep='\n')
    print('Solution Length: {}'.format(len(solution) - 1))


def init_seeds(amount):
    """
    The function init 20 different seeds for comparing the algorithms
    :param amount: int, amount of seeds
    :return: list with all the seeds
    """

    i = 48
    seeds = []

    while len(seeds) < amount:

        rnd_table = EightPuzzle.init_table(seed=i)

        if EightPuzzle.is_solvable(rnd_table):
            seeds.append(i)

        i += 1

    return seeds


def compare_algorithms():
    """
    The function compare between A* and B&B algorithms using two different heuristics.
    Both algorithms compare according to 20 different init tables.
    :return:
    """

    seeds = init_seeds(amount=20)

    a_star = {'manhattan': [], 'misplace': []}
    bnb = {'manhattan': [], 'misplace': []}

    for s in seeds:

        print('---- Seed = {} ----'.format(s))

        init_state = EightPuzzle.init_table(seed=s)

        puzzle = EightPuzzle(init_state, goal_state)

        # A* with manhattan
        print('A* & Manhattan')
        start = time()
        puzzle.solve('A*', h_manhattan)
        a_star['manhattan'].append(time() - start)

        # A* with misplace
        print('A* & Misplace')
        start = time()
        puzzle.solve('A*', h_misplaced)
        a_star['misplace'].append(time() - start)

        # B&B with manhattan
        print('B&B & Manhattan')
        start = time()
        puzzle.solve('BnB', h_manhattan)
        bnb['manhattan'].append(time() - start)

        # B&B with misplace
        print('B&B & Misplace')
        start = time()
        puzzle.solve('BnB', h_misplaced)
        bnb['misplace'].append(time() - start)

    print('A*: {}'.format(a_star))
    print('BnB: {}'.format(bnb))


if __name__ == '__main__':

    # main()

    compare_algorithms()


