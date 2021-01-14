import numpy as np
from copy import deepcopy


class Backtracking:

    def __init__(self, n_variables, n_domain, constraints):

        self.n_variables = n_variables
        self.n_domain = n_domain
        self.constraints = constraints

    def solve(self):

        # Init variables' values as `None`
        solution = {i: None for i in range(self.n_variables)}

        # Init variables' domain as full
        domains = {i: range(self.n_domain) for i in self.n_variables}

        # Make assignment for all variables recursively
        solution = self.assign_variable(1, domains, solution)

        return solution

    def assign_variable(self, variable, domains, solution):

        # If we need to assign value for variable 1 and his domain his empty -
        # there is no solution so return `None`
        if (variable == 1) & (len(domains[variable]) == 0):

            return None

        # If we need to assign value for variable we don't have -
        # we can return the solution
        if variable > self.n_variables:

            return solution

        # Else - look for legal value for the current variable
        value, domains = self.find_legal_value(variable, domains, deepcopy(solution))

        if value is None:

            domains[variable] = range(self.n_domain)

            return self.assign_variable(variable - 1, domains, solution)

        else:
            solution[variable] = value
            return self.assign_variable(variable + 1, domains, solution)

    def find_legal_value(self, variable, domains, solution):

        for value in domains[variable]:

            domains[variable].remove(value)  # remove the value from the domain
            solution[variable] = value  # update solution

            if self.is_legal_solution(solution):

                return value, domains

        return None, domains

    def is_legal_solution(self, solution):

        pass






