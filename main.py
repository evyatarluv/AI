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


def solve_puzzle():
    """
    The main function initialize a random (solvable) table and print the solution.
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
    plt.show()


def plot_algorithms():

    results = {
        'A*': [0.1322612762451172, 0.009804487228393555, 0.11649560928344727, 1.3041791915893555, 0.18230581283569336,
               6.8320698738098145, 0.972710132598877, 0.4562492370605469, 1.3408029079437256, 2.2559170722961426,
               0.03904223442077637, 1.0241806507110596, 0.18136262893676758, 0.9769155979156494, 9.160584688186646,
               1.0153982639312744, 1.4064521789550781, 12.78885293006897, 10.135646343231201, 0.1546320915222168,
               9.29797911643982, 0.3927278518676758, 0.36492919921875, 1.307647466659546, 0.3090200424194336,
               0.021553993225097656, 0.21794986724853516, 2.873443365097046, 13.802127361297607, 0.5875759124755859,
               3.631507158279419, 2.490621566772461, 0.09400510787963867, 0.17684125900268555, 1.616575002670288,
               0.30843520164489746, 1.1270194053649902, 1.1012070178985596, 0.06257390975952148, 0.5162613391876221,
               1.4223828315734863, 1.3266499042510986, 0.13009095191955566, 0.39998745918273926, 0.6978769302368164,
               0.1554107666015625, 0.10867595672607422, 0.22640442848205566, 0.19286084175109863, 1.2551538944244385],
        'B&B': [0.21613216400146484, 0.005052328109741211, 0.07908320426940918, 1.3150031566619873, 0.15178179740905762,
                1.803821325302124, 1.2471375465393066, 0.4415090084075928, 0.5271542072296143, 0.9761786460876465,
                0.038593292236328125, 0.6183528900146484, 0.25754880905151367, 0.40047764778137207, 7.6815197467803955,
                0.34372472763061523, 1.0524137020111084, 4.211444616317749, 2.8023464679718018, 0.1697864532470703,
                4.772823095321655, 0.39870429039001465, 0.63201904296875, 1.2778828144073486, 0.2809872627258301,
                0.03381824493408203, 0.12406110763549805, 1.3511521816253662, 3.995889186859131, 0.6169216632843018,
                2.5277388095855713, 2.4027793407440186, 0.07195186614990234, 0.16091656684875488, 1.1304841041564941,
                0.22599387168884277, 1.3140292167663574, 0.9437541961669922, 0.041144609451293945, 0.4905862808227539,
                0.6787917613983154, 0.6941583156585693, 0.12027263641357422, 0.20220446586608887, 0.5171349048614502,
                0.142897367477417, 0.10763716697692871, 0.19384503364562988, 0.06824946403503418, 0.7711281776428223]
    }

    plt.scatter(range(len(results['A*'])), results['A*'], label='A*')
    plt.scatter(range(len(results['A*'])), results['B&B'], label='B&B')
    plt.legend()
    plt.show()

    # Create DataFrame from the result dict
    # results_df = pd.DataFrame(columns=['Run Time', 'Algorithm'])
    # for algo in results:
    #     for run_time in results[algo]:
    #         results_df = results_df.append({'Run Time': run_time, 'Algorithm': algo}, ignore_index=True)
    #
    # sns.boxplot(x='Algorithm', y='Run Time', data=results_df)
    # plt.show()


def plot_comparison():

    # plot_heuristics()

    plot_algorithms()


if __name__ == '__main__':
    # solve_puzzle()

    # compare_algorithms()

    plot_comparison()
