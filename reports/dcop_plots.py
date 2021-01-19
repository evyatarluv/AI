import pickle
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt


def compare_p2():

    # Read the results
    path = 'results/compare_p2/{}.pickle'
    dsa: Dict[float, List] = pickle.load(open(path.format('dsa'), 'rb'))
    mgm2: Dict[float, List] = pickle.load(open(path.format('mgm2'), 'rb'))
    p2 = [round(v, 2) for v in dsa.keys()]

    # Plot
    # DSA
    dsa_means = [np.mean(lst) for lst in dsa.values()]
    dsa_stds = [np.std(lst) for lst in dsa.values()]
    plt.errorbar(p2, dsa_means, yerr=dsa_stds, capsize=2.5, fmt='-o', label='DSA-C')

    # MGM2
    mgm2_means = [np.mean(lst) for lst in mgm2.values()]
    mgm2_stds = [np.std(lst) for lst in mgm2.values()]
    plt.errorbar(p2, mgm2_means, yerr=mgm2_stds, capsize=2.5, fmt='-o', label='MGM2')

    # Aesthetic things
    plt.grid(axis='y')
    plt.legend()
    plt.ylabel('Sum of Costs')
    plt.xlabel(r'$p_2$')
    plt.title(r'Compare $p_2$ Influence ($p_1$ = 0.2)')
    plt.show()


def compare_iterations():

    # Read the results
    path = 'results/compare_iterations/{}.pickle'
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
    plt.plot(iterations, dsa_mean, label='DSA-C')
    plt.plot(iterations, mgm2_mean, label='MGM2')
    plt.grid(axis='y')
    plt.legend()
    plt.ylabel('Sum of Costs')
    plt.xlabel('Iterations/Cycles')
    plt.title('DSA-C VS. MGM2')
    plt.show()


if __name__ == '__main__':

    # compare_p2()
    
    compare_iterations()
