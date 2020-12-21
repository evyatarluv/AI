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

    # Choose h function
    h_functions = {'ma': h_manhattan, 'e': h_euclidean, 'mi': h_misplaced}
    while True:

        try:
            user_h = input(
                'Please choose heuristic function - manhattan (ma), euclidean (e) or misplace (mi)\n').lower()
            h_function = h_functions[user_h]
            break

        except KeyError:

            print('Please choose one of the requested letters')

    return algorithm, h_function


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
    algorithm, h_function = user_choose_solver()

    # Solve the init table
    puzzle = EightPuzzle(init_state, goal_state)
    solution = puzzle.solve(algorithm, h_function)

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

    seeds = []

    while len(seeds) < amount:

        s = np.random.randint(0, 5000)
        rnd_table = EightPuzzle.init_table(seed=s)

        if EightPuzzle.is_solvable(rnd_table):
            seeds.append(s)

    return seeds


def compare_algorithms(comparisons_amount):
    """
    The function compare between A* and B&B algorithms using two different heuristics.
    Both algorithms compare according to given amount of different init tables.
    :param comparisons_amount: int, the amount of comparisons for the algorithms
    :return:
    """

    seeds = init_seeds(amount=comparisons_amount)

    a_star = {'manhattan': [], 'euclidean': []}
    bnb = {'manhattan': [], 'euclidean': []}

    for s in seeds:
        print('---- Seed = {} ----'.format(s))

        init_state = EightPuzzle.init_table(seed=s)

        puzzle = EightPuzzle(init_state, goal_state)

        # A* with manhattan
        print('A* & Manhattan')
        start = time()
        puzzle.a_star_solve(h_manhattan, False)
        a_star['manhattan'].append(time() - start)

        # A* with euclidean
        print('A* & Euclidean')
        start = time()
        puzzle.a_star_solve(h_euclidean, False)
        a_star['euclidean'].append(time() - start)

        # B&B with manhattan
        print('B&B & Manhattan')
        start = time()
        puzzle.bnb_solve(h_manhattan, 'dfs', False, init_ub=31)
        bnb['manhattan'].append(time() - start)

        # B&B with euclidean
        print('B&B & Euclidean')
        start = time()
        puzzle.bnb_solve(h_euclidean, 'dfs', False, init_ub=31)
        bnb['euclidean'].append(time() - start)

    print('A*:\nmanhattan: {}\neuclidean: {}'.format(a_star['manhattan'], a_star['euclidean']))
    print('BnB:\nmanhattan: {}\neuclidean: {}'.format(bnb['manhattan'], bnb['euclidean']))


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
        for run_time in bnb[heuristic]:
            results = results.append({'Run Time': run_time, 'Algorithm': 'B&B', 'Heuristic': heuristic},
                                     ignore_index=True)

    # Debug: print the dataframe
    # print(results)

    return results


def plot_run_times():

    a_star = {'Manhattan': np.loadtxt("figures_data/run_times/astar_manhattan.txt", delimiter=",", unpack=False),
              'Euclidean': np.loadtxt("figures_data/run_times/astar_euclidean.txt", delimiter=",", unpack=False)}

    bnb = {'Manhattan': np.loadtxt("figures_data/run_times/bnb_manhattan.txt", delimiter=",", unpack=False),
           'Euclidean': np.loadtxt("figures_data/run_times/bnb_euclidean.txt", delimiter=",", unpack=False)}

    # Convert dictionaries to dataframe
    results = results_dataframe(a_star, bnb)

    # Plots
    sns.set_style('whitegrid')
    sns.boxplot(x='Algorithm', y='Run Time', hue='Heuristic', data=results, showfliers=False, palette='Set3')
    plt.ylabel('Run Time (s)')
    plt.title('A* vs. B&B - Run Time')
    plt.show()


def plot_comparison():

    plot_depths()

    plot_run_times()


def plot_depths():
    bfs = np.loadtxt("figures_data/depths/depths_bfs.txt", comments="#", delimiter=",", unpack=False)
    dfs = np.loadtxt("figures_data/depths/depths_dfs.txt", comments="#", delimiter=",", unpack=False)
    a_star = np.loadtxt("figures_data/depths/depths_astar.txt", comments="#", delimiter=",", unpack=False)

    fig, axs = plt.subplots(2)

    # Plot
    axs[0].plot(a_star)
    axs[1].plot(dfs, label='Current Depth')

    # Add titles
    axs[0].set_title('A* - Best-First')
    axs[1].set_title('B&B - DFS')

    # Add axis-labels
    axs[0].set_xlabel('Iterations')
    axs[1].set_xlabel('Iterations')
    axs[1].set_ylabel('Depth')
    axs[0].set_ylabel('Depth')

    for ax in axs:
        ax.set_xticks([])
        ax.axhline(17, color='red', linestyle='--', label='Solution Depth')

    axs[1].legend(loc='lower right', bbox_to_anchor=(1, 1))

    plt.show()


if __name__ == '__main__':

    # Solve a random single 8-puzzle and print the solution
    solve_puzzle()

    # Compare algorithms solving the 8-puzzle
    # compare_algorithms(comparisons_amount=30)

    # Plot comparison figures
    # plot_comparison()
