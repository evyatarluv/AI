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
    # fig, (dsa_ax, mgm2_ax) = plt.subplots(1, 2)

    # DSA
    dsa_means = [np.mean(lst) for lst in dsa.values()]
    dsa_stds = [np.std(lst) for lst in dsa.values()]
    plt.errorbar(p2, dsa_means, yerr=dsa_stds, capsize=2.5, fmt='-o', label='DSA')

    # MGM2
    mgm2_means = [np.mean(lst) for lst in mgm2.values()]
    mgm2_stds = [np.std(lst) for lst in mgm2.values()]
    plt.errorbar(p2, mgm2_means, yerr=mgm2_stds, capsize=2.5, fmt='-o', label='MGM2')

    # Aesthetic things
    plt.grid(axis='y')
    plt.legend()
    plt.ylabel('Sum of Costs')
    plt.xlabel(r'$p_2$')
    plt.title(r'Compare $p_2$ Influence')
    plt.show()


if __name__ == '__main__':

    compare_p2()
