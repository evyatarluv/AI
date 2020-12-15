import numpy as np
from Node import Node
import random as rnd
import sys


def reconstruct_solution(solution):

    solution_list = [solution]
    node = solution.parent

    while node is not None:

        solution_list.insert(0, node)
        node = node.parent

    return solution_list


def print_status(iteration, open_list_length):

    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write('Status: Iteration = {}, Open List Length = {}'.format(iteration, open_list_length))
    sys.stdout.flush()


class EightPuzzle:

    def __init__(self, init_state, goal_state):

        self.init_state = Node(init_state, 0, None)

        self.goal_state = goal_state

        self.solution = None

    def solve(self, algorithm, h_function):
        """
        This method get an algorithm name to solve the eight-puzzle, and heuristic function.
        The method return a solution.
        :param algorithm: str, algorithm name
        :param h_function: function which get current table (matrix) and goal state (matrix)
                            and return scalar
        :return: solution as Node object or None if there is no solution
        """

        # print('Using {} to solve the 8-puzzle...'.format(algorithm))
        # print('Init table: \n{}'.format(self.init_state))

        if algorithm == 'BnB':
            self.bnb_solve(h_function)

        elif algorithm == 'A*':
            self.a_star_solve(h_function)

        else:
            raise NameError('Unused algorithm, please choose `BnB` or `A*`.')

        return reconstruct_solution(self.solution)

    def bnb_solve(self, h_function, verbose=True):
        """
        This method implement Branch & Bound algorithm.
        The B&B implementation using priority queue for the open list.
        :param verbose: bool, if to print log messages
        :param h_function: heuristic function for the LB
        :return: solution (Node)
        """

        # Init params
        solution = None
        open_list = [self.init_state]
        close_set = set()
        ub = np.inf
        iterations = 0

        # Verbose
        if verbose:
            print('Got my init state: \n {}'.format(self.init_state))
            print('Start working to find solution using B&B...')

        while len(open_list) > 0:

            # Verbose the status
            if verbose:
                iterations += 1
                if iterations % 300 == 0:
                    print_status(iterations, len(open_list))

            # Get the current parent node for this iteration
            parent = open_list.pop(0)
            current_children = []
            parent_depth = parent.depth()

            # Iteration status
            iterations += 1
            if iterations > 5000 == 0:
                print('This is a taught one...', end='\r')

            # Branch
            for child in parent.expand():

                # If this children is the goal state
                if (child == self.goal_state).all():

                    # If this solution is better then the current solution
                    if parent_depth + 1 < ub:
                        ub = parent_depth + 1
                        solution = Node(child, ub, parent)

                # Bound
                else:
                    if tuple(child.flatten()) not in close_set:

                        lb = parent_depth + 1 + h_function(child, self.goal_state)

                        if lb < ub:
                            current_children.append(Node(child, lb, parent))

            # Update open list
            open_list = current_children + open_list
            open_list.sort(key=lambda x: x.lb)

            # Update close set
            close_set.add(tuple(parent.table.flatten()))

        self.solution = solution

    def a_star_solve(self, h_function, verbose=True):

        """
        This method implement A* algorithm.
        :param verbose: bool, if to print log messages
        :param h_function: heuristic function for f function.
        :return: solution (Node)
        """

        # Init params
        solution = None
        open_list = [self.init_state]
        close_set = set()
        iterations = 0

        # Verbose
        if verbose:
            print('Got my init state: \n{}'.format(self.init_state))
            print('Start working to find solution using A*...\n')

        while len(open_list) > 0:

            # Verbose the status
            if verbose:
                iterations += 1
                if iterations % 300 == 0:
                    print_status(iterations, len(open_list))

            # Get the current parent node for this iteration
            parent = open_list.pop(0)
            g_value = parent.depth() + 1

            # Expand node
            for child in parent.expand():

                # If this children is the goal state - this is an optimal solution
                if (child == self.goal_state).all():
                    self.solution = Node(child, g_value, parent)
                    return

                # If not a solution
                else:
                    if tuple(child.flatten()) not in close_set:

                        f_value = g_value + h_function(child, self.goal_state)
                        open_list.append(Node(child, f_value, parent))

            # Best-First: sort the open list
            open_list.sort(key=lambda x: x.lb)

            # Update close set
            close_set.add(tuple(parent.table.flatten()))

        self.solution = solution

    @staticmethod
    def is_solvable(table):
        """
        Check if a given init table is solvable
        :param table: init table
        :return: bool answer
        """

        count = 0
        table = table.flatten()

        for i in range(len(table)):
            for j in range(i + 1, len(table)):
                if (table[i] > table[j]) & (table[j] != 0):
                    count += 1

        return count % 2 == 0

    @staticmethod
    def init_table(seed=None):
        """
        This function create initial state of the 8-table.
        The function return only solvable init table.
        :param seed: seed to the random function, optional
        :return:
        """

        if seed is not None:
            rnd.seed(seed)

        table = np.array(rnd.sample(range(9), 9)).reshape((3, 3))

        while not EightPuzzle.is_solvable(table):
            table = np.array(rnd.sample(range(9), 9)).reshape((3, 3))

        return table
