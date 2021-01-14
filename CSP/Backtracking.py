from typing import List, Dict, Tuple
import numpy as np
from copy import copy
import matplotlib.pyplot as plt


class Variable:
    """
    Class representing variable in the problem

    Attributes:
        id:
            the id of the variable

        domain:
            list with the domain of the variable

        current_domain:
            list with the current domain of the variables, after removing according to constraints

        value:
            the assignment of the variable
    """
    def __init__(self, variable_id, domain, value):

        self.id: int = variable_id
        self.domain: List[int] = copy(domain)
        self.current_domain: List[int] = copy(domain)
        self.value = value

    def reset_domain(self):
        """
        reset the current domain of the variable to be as the original domain
        :return:
        """
        self.current_domain = copy(self.domain)

    def __str__(self):

        return 'X{}'.format(self.id)


class Backtracking:
    """
    A class for solving the CSP problem using backtracking algorithm

    Attributes:

        n_variables:
            number of variables in the problem

        n_domain:
            number of element in the domain for each variable in the problem

        constraints:
            the constraints of the problem, in the form of (x1, value, x2, value), each constraint
            is a forbidden assignment
    """
    def __init__(self, n_variables, n_domain, constraints):

        self.n_variables: int = n_variables
        self.n_domain: int = n_domain
        self.constraints: set = constraints

    def solve(self):

        print('Start solving CSP using BT algorithm...\n')

        # Init solution as variables with `None`
        domain = list(range(self.n_domain))
        solution = {i: Variable(i, domain, None) for i in range(1, self.n_variables + 1)}

        # Make assignment for all variables recursively
        solution = self.assign_variables(1, solution)

        return solution

    def assign_variables(self, variable, solution: Dict[int, Variable]):

        # If we need to assign value for variable we don't have -
        # we can return the solution
        if variable > self.n_variables:

            return solution

        # If we need to assign value for variable 1 and his domain his empty -
        # there is no solution so return `None`
        if (variable == 1) & (len(solution[variable].current_domain) == 0):

            return None

        # Else - look for legal value for the current variable
        value = self.find_legal_value(variable, solution)

        if value is None:

            solution[variable].reset_domain()

            return self.assign_variables(variable - 1, solution)

        else:

            solution[variable].value = value
            return self.assign_variables(variable + 1, solution)

    def find_legal_value(self, variable: int, solution: Dict[int, Variable]):

        variable_domain = copy(solution[variable].current_domain)

        for value in solution[variable].current_domain:

            legal = True

            for other_variable in range(1, variable):

                # Check if constraint like this exist
                constraint = [(variable, value, other_variable, solution[other_variable].value),
                              (other_variable, solution[other_variable].value, variable, value)]

                if any(c in self.constraints for c in constraint):

                    legal = False
                    break

            # Remove
            variable_domain.remove(value)

            if legal:

                solution[variable].current_domain = copy(variable_domain)
                return value

        return None










