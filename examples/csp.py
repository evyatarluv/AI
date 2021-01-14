import os
import sys

import numpy as np
from pathlib import Path
import yaml
from CSP.Backtracking import Backtracking
from CSP.generate_constraints import generate_constraints
import matplotlib.pyplot as plt

# Project root directory
root_directory = Path(__file__).parent.parent

# Change recursion limit
sys.setrecursionlimit(10**6)


def main():

    # Load configuration file
    config_path = os.path.join(root_directory, 'CSP/config.yaml')
    config = yaml.full_load(open(config_path))

    # Params
    n_variables = config['environment']['n_variables']
    n_constraints = config['environment']['n_constraints']
    n_domain = config['environment']['n_domain']
    algorithm = config['environment']['algorithm']
    seed = config['environment']['seed']

    # generate constraints
    np.random.seed(seed)
    constraints = generate_constraints(n_variables, n_domain, n_constraints)
    constraints.add((1, 0, 2, 0))

    # Solve
    solution = None
    if algorithm.lower() in ['bt', 'backtracking']:

        bt = Backtracking(n_variables, n_domain, constraints)

        solution = bt.solve()

    # Print solution
    if solution is not None:

        print('Solution: {}'.format([x.value for x in solution.values()]))

    else:

        print('No solution')

    plt.plot(bt.search_path)
    plt.show()





if __name__ == '__main__':

    main()