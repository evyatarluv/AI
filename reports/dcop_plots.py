import pickle
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt


def compare_p2():

    fig, (p1_02, p1_05) = plt.subplots(1, 2)

    for p1_value, ax in [(0.2, p1_02), (0.5, p1_05)]:

        # Read the results
        path = 'results/compare_p2/p1_' + str(p1_value).replace('.', '') + '/{}.pickle'
        dsa: Dict[float, List] = pickle.load(open(path.format('dsa'), 'rb'))
        mgm2: Dict[float, List] = pickle.load(open(path.format('mgm2'), 'rb'))
        p2 = [round(v, 2) for v in dsa.keys()]

        # Plot
        # DSA
        dsa_means = [np.mean(lst) for lst in dsa.values()]
        dsa_stds = [np.std(lst) for lst in dsa.values()]
        ax.errorbar(p2, dsa_means, yerr=dsa_stds, capsize=2.5, fmt='-o', label='DSA-C')

        # MGM2
        mgm2_means = [np.mean(lst) for lst in mgm2.values()]
        mgm2_stds = [np.std(lst) for lst in mgm2.values()]
        ax.errorbar(p2, mgm2_means, yerr=mgm2_stds, capsize=2.5, fmt='-o', label='MGM2')

        # Aesthetic things
        ax.grid(axis='y')
        ax.legend()
        ax.set_ylabel('Sum of Costs')
        ax.set_xlabel(r'$p_2$')
        ax.set_title(r'$p_1$ = {}'.format(p1_value))

    # fig.suptitle(r'Compare $p_2$ Influence')
    plt.show()


def compare_iterations():

    fig, (p1_02, p1_05) = plt.subplots(1, 2)

    for p1_value, ax in [(0.2, p1_02), (0.5, p1_05)]:

        # Read the results
        path = 'results/compare_iterations/p1_' + str(p1_value).replace('.', '') + '/{}.pickle'
        dsa: Dict[int, List] = pickle.load(open(path.format('dsa'), 'rb'))
        mgm2: Dict[int, List] = pickle.load(open(path.format('mgm2'), 'rb'))
        iterations = list(range(0, 1000, 10))

        # DSA
        # Get mean & std
        dsa_mean = np.array(list(dsa.values())).mean(axis=0)
        dsa_std = np.array(list(dsa.values())).std(axis=0)

        # Down sample the vector
        dsa_mean = [dsa_mean[i] for i in range(0, len(dsa_mean), 10)]
        dsa_std = [dsa_std[i] for i in range(0, len(dsa_std), 10)]

        # MGM2
        # Get mean & std
        mgm2_mean = np.array(list(mgm2.values())).mean(axis=0)
        mgm2_std = np.array(list(mgm2.values())).std(axis=0)

        # Down sample the vector
        mgm2_mean = [mgm2_mean[i] for i in range(0, len(mgm2_mean), 50)]
        mgm2_std = [mgm2_std[i] for i in range(0, len(mgm2_std), 50)]

        # Plot
        # fig, (dsa_ax, mgm2_ax) = plt.subplots(1, 2, sharey=True)
        # plt.errorbar(iterations, dsa_mean, yerr=dsa_std, capsize=2.5, fmt='-o', label='DSA-C')
        # plt.errorbar(iterations, mgm2_mean, yerr=mgm2_std, capsize=2.5, fmt='-o', label='MGM2')
        ax.plot(iterations, dsa_mean, label='DSA-C')
        ax.plot(iterations, mgm2_mean, label='MGM2')
        ax.grid(axis='y')
        ax.legend()
        ax.set_ylabel('Sum of Costs')
        ax.set_xlabel('Iterations/Cycles')
        ax.set_title(r'$p_1$ = {}'.format(p1_value))

    plt.show()


if __name__ == '__main__':

    compare_p2()
    
    # compare_iterations()
