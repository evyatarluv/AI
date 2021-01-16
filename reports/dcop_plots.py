import pickle
from typing import List, Dict

import numpy as np
import matplotlib.pyplot as plt


def compare_p2():

    # Read the results
    path = 'results/compare_p2/{}.pickle'
    dsa: Dict[float, List] = pickle.load(open(path.format('dsa'), 'rb'))
    # mgm2 = pickle.load(open(path.format('mgm2'), 'rb'))
    p2 = [round(v, 2) for v in dsa.keys()]

    # Plot
    # DSA
    dsa_means = [np.mean(lst) for lst in dsa.values()]
    dsa_stds = [np.std(lst) for lst in dsa.values()]
    plt.errorbar(p2, dsa_means, yerr=dsa_stds, capsize=2.5, fmt='-o')
    plt.show()


if __name__ == '__main__':

    compare_p2()
