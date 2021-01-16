import pickle

import matplotlib.pyplot as plt


def compare_p2():

    # Read the results
    path = 'results/compare_p2/{}.pickle'
    dsa = pickle.load(open(path.format('dsa'), 'rb'))
    # mgm2 = pickle.load(open(path.format('mgm2'), 'rb'))

    # Plot
    # DSA



if __name__ == '__main__':

    compare_p2()
