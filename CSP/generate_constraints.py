import numpy as np


def generate_constraints(n_variables: int, n_domain: int, n_constraints: int) -> set:

    print('Generating constraints...\n')

    constraints = set()

    while len(constraints) < n_constraints:

        variables = np.random.choice(range(n_variables), 2, replace=False)

        values = np.random.choice(range(n_domain), 2, replace=False)

        constraints.add((variables[0], values[0], variables[1], values[1]))

    return constraints

