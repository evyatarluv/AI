from typing import List, Dict, Tuple

import numpy as np
from copy import deepcopy


class Variable:

    def __init__(self, variable_id, domain, value):

        self.id: int = variable_id
        self.domain: List[int] = deepcopy(domain)
        self.current_domain: List[int] = deepcopy(domain)
        self.value = value

    def reset_domain(self):

        self.current_domain = deepcopy(self.domain)

    # todo: use property for current domain


class Backtracking:

    def __init__(self, n_variables, n_domain, constraints):

        self.n_variables: int = n_variables
        self.n_domain: int = n_domain
        self.constraints: set = constraints

    def solve(self):

        # Init solution as variables with `None`
        domain = range(self.n_domain)
        solution = {i: Variable(i, domain, None) for i in range(self.n_variables)}

        # Make assignment for all variables recursively
        solution = self.assign_variable(1, solution)

        return solution

    def assign_variable(self, variable, solution: Dict[int, Variable]):

        # If we need to assign value for variable 1 and his domain his empty -
        # there is no solution so return `None`
        if (variable == 1) & (len(solution[variable].current_domain) == 0):

            return None

        # If we need to assign value for variable we don't have -
        # we can return the solution
        if variable > self.n_variables:

            return solution

        # Else - look for legal value for the current variable
        value = self.find_legal_value(variable, solution)

        if value is None:

            solution[variable].reset_domain()

            return self.assign_variable(variable - 1, solution)

        else:

            solution[variable].value = value
            return self.assign_variable(variable + 1, solution)

    def find_legal_value(self, variable: int, solution: Dict[int, Variable]):

        variable_domain = deepcopy(solution[variable].current_domain)

        for value in solution[variable].current_domain:

            legal = True

            for other_variable in range(1, variable):

                # Check if constraint like this exist
                constraint = (variable, value, other_variable, solution[other_variable].value)

                if constraint in self.constraints:

                    legal = False
                    variable_domain.remove(value)
                    break

            if legal:

                solution[variable].current_domain = deepcopy(variable_domain)
                return value

        return None










