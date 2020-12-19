import numpy as np
from EightPuzzle import EightPuzzle
import random as rnd
from heuristics import *
from time import time
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

goal_state = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 0]])


def user_choose_solver():
    """
    The function get from the user the the algorithm to work with.
    If the user chose B&B we need to get also the search type.

    :return: algorithm and search type as str
    """

    # Choose algorithm
    algorithms = {'a': 'A*', 'b': 'bnb'}
    while True:

        try:
            user_algo = input('Please choose your algorithm - A* (a) or B&B (b)\n')
            algorithm = algorithms[user_algo]
            break

        except KeyError:
            print('Please choose one of the requested letters')

    # Choose search type
    if algorithm == 'bnb':
        types = {'d': 'dfs', 'b': 'bfs'}

        while True:
            try:
                user_type = input('DFS (d) or BFS (b)?\n').lower()
                search_type = types[user_type]
                break
            except KeyError:
                print('Please choose one of the requested letters')
    else:
        search_type = None

    # Choose h function
    h_functions = {'ma': h_manhattan, 'e': h_euclidean, 'mi': h_misplaced}
    while True:

        try:
            user_h = input('Please choose heuristic function - manhattan (ma), euclidean (e) or misplace (mi)\n').lower()
            h_function = h_functions[user_h]
            break

        except KeyError:

            print('Please choose one of the requested letters')

    return algorithm, search_type, h_function


def solve_puzzle():

    """
    This function is an interactive 8-puzzle solver.
    The user can define a init table, or rand one.
    Then the user choose an algorithm which solve the puzzle.
    The solver return the solution and the function print it.
    :return:
    """

    # Init solvable table
    init_state = EightPuzzle.init_table()

    # Get the user solver preferences
    algorithm, search_type, h_function = user_choose_solver()

    # Solve the init table
    puzzle = EightPuzzle(init_state, goal_state)
    solution = puzzle.solve(algorithm, h_function, search_type)

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

    i = 103
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
    Both algorithms compare according to given amount of different init tables.
    :return:
    """

    seeds = init_seeds(amount=50)

    a_star = {'manhattan': [], 'euclidean': []}
    bnb = {'manhattan': [], 'euclidean': []}

    for s in seeds:
        print('---- Seed = {} ----'.format(s))

        init_state = EightPuzzle.init_table(seed=s)

        puzzle = EightPuzzle(init_state, goal_state)

        # A* with manhattan
        print('A* & Manhattan')
        start = time()
        puzzle.solve('A*', h_manhattan)
        a_star['manhattan'].append(time() - start)

        # A* with euclidean
        print('A* & Euclidean')
        start = time()
        puzzle.solve('A*', h_euclidean)
        a_star['euclidean'].append(time() - start)

        # B&B with manhattan
        print('B&B & Manhattan')
        start = time()
        puzzle.solve('BnB', h_manhattan)
        bnb['manhattan'].append(time() - start)

        # B&B with euclidean
        print('B&B & Euclidean')
        start = time()
        puzzle.solve('BnB', h_euclidean)
        bnb['euclidean'].append(time() - start)

    print('A*: {}'.format(a_star))
    print('BnB: {}'.format(bnb))


def results_dataframe(a_star, bnb):
    """
    Reconstruct the results as dataframe
    :param a_star: dict with {'heuristic': [run_times]}
    :param bnb: dict with {'heuristic': [run_times]}
    :return:
    """

    results = pd.DataFrame(columns=['Run Time', 'Algorithm', 'Heuristic'])

    for heuristic in a_star:
        for run_time in a_star[heuristic]:
            results = results.append({'Run Time': run_time, 'Algorithm': 'A*', 'Heuristic': heuristic},
                                     ignore_index=True)

    for heuristic in bnb:
        for run_time in a_star[heuristic]:
            results = results.append({'Run Time': run_time, 'Algorithm': 'B&B', 'Heuristic': heuristic},
                                     ignore_index=True)

    # Debug: print the dataframe
    # print(results)

    return results


def plot_heuristics():

    a_star = {'Manhattan': [0.09871149063110352, 0.13067626953125, 0.7476649284362793,
                            0.024929285049438477, 0.4218897819519043, 0.09474515914916992, 0.33011531829833984,
                            0.06250691413879395, 0.04688739776611328, 0.4061143398284912,
                            0.4061288833618164, 0.04686331748962402, 1.7651846408843994, 0.07810592651367188,
                            0.1601276397705078, 0.0153961181640625, 0.3796401023864746, 0.4100658893585205],
              'Euclidean': [0.17253756523132324, 0.1575782299041748, 1.131971836090088,
                            0.03191494941711426, 1.676586389541626, 0.1436169147491455, 0.4866983890533447,
                            0.26553797721862793, 0.07808089256286621, 0.9060389995574951,
                            0.6560952663421631, 0.12497186660766602, 2.9992942810058594, 0.14061641693115234,
                            0.20353388786315918, 0.0050182342529296875, 0.9002478122711182, 0.6849789619445801]}

    bnb = {'Manhattan': [0.1406230926513672, 0.12566328048706055, 0.2872292995452881, 2.813910961151123,
                         0.01994633674621582, 0.5666520595550537, 0.12366795539855957, 0.28024983406066895,
                         2.510826587677002, 0.1249704360961914, 0.03124237060546875, 0.2812058925628662,
                         0.39055514335632324, 0.06246161460876465, 2.1870031356811523, 0.06246066093444824,
                         0.11495161056518555, 0.005006551742553711, 0.429948091506958, 0.43488597869873047],
           'Euclidean': [0.24933290481567383, 0.2263939380645752, 1.5458669662475586,
                         0.05086374282836914, 2.319847583770752, 0.2313826084136963, 0.8857347965240479,
                         0.3905346393585205, 0.12501001358032227, 1.2340850830078125,
                         0.9841430187225342, 0.17185616493225098, 0.23843598365783691,
                         0.2849304676055908, 0.010022401809692383, 1.2800819873809814, 0.9550232887268066]}

    results = results_dataframe(a_star, bnb)

    sns.boxplot(x='Algorithm', y='Run Time', hue='Heuristic', data=results, palette="Set3")
    plt.title('Compare Algorithms & Heuristic')
    plt.show()


def plot_algorithms():

    results = {
        'A*': [0.09871149063110352, 0.13067626953125, 0.7476649284362793,
                            0.024929285049438477, 0.4218897819519043, 0.09474515914916992, 0.33011531829833984,
                            0.06250691413879395, 0.04688739776611328, 0.4061143398284912,
                            0.4061288833618164, 0.04686331748962402, 1.7651846408843994, 0.07810592651367188,
                            0.1601276397705078, 0.0153961181640625, 0.3796401023864746, 0.4100658893585205],
        'B&B': [0.1406230926513672, 0.12566328048706055, 0.2872292995452881, 2.813910961151123,
                         0.01994633674621582, 0.5666520595550537, 0.12366795539855957, 0.28024983406066895,
                         2.510826587677002, 0.1249704360961914, 0.03124237060546875, 0.2812058925628662,
                         0.39055514335632324, 0.06246161460876465, 2.1870031356811523, 0.06246066093444824,
                         0.11495161056518555, 0.005006551742553711, 0.429948091506958, 0.43488597869873047]
    }

    # Create DataFrame from the result dict
    results_df = pd.DataFrame(columns=['Run Time', 'Algorithm'])
    for algo in results:
        for run_time in results[algo]:
            results_df = results_df.append({'Run Time': run_time, 'Algorithm': algo}, ignore_index=True)

    sns.boxplot(x='Algorithm', y='Run Time', data=results_df, palette='Set3')
    plt.title('Compare Algorithms - Heuristic: Manhattan Distance')
    plt.show()


def plot_comparison():

    plot_heuristics()

    plot_algorithms()


if __name__ == '__main__':

    # Solve a random single 8-puzzle and print the solution
    # solve_puzzle()

    # Compare algorithms solving the 8-puzzle
    # compare_algorithms()

    # Plot comparison figures
    # plot_comparison()

    pass

# My play zone
init = np.array([5,3,0,2,4,1,7,8,6]).reshape((3,3))
p = EightPuzzle(init, goal_state)
print('Solution Length: {}'.format(len(p.solve('bnb', h_manhattan, search_type='dfs', verbose=True)) - 1))
