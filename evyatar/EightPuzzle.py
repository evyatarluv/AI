import copy
import numpy as np
from .Node import Node
import time


def is_node_exist(table, existed_set):
    """
    This function get two lists and return if the table is in on of those lists
    :param table: ndarray represent the table
    :param existed_set: set with the existed nodes
    :return: bool answer if the table appear in the existed list
    """

    # Check if this table already exist
    return table in existed_set


def reconstruct_solution(solution):

    solution_list = [solution.table]
    node = solution.parent

    while node is not None:

        solution_list.insert(0, node.table)
        node = node.parent

    return solution_list


class EightPuzzle:

    def __init__(self, init_state, goal_state):

        self.init_state = Node(init_state, 0, 0, None)

        self.goal_state = goal_state

        self.solution = None

    def solve(self, method, h_function):
        """
        This method get an algorithm name to solve the eight-puzzle, and heuristic function.
        The method return a solution.
        :param method: str, algorithm name
        :param h_function: function which get current table (matrix) and goal state (matrix)
                            and return scalar
        :return: solution as Node object
        """

        if method == 'BnB':
            self.bnb_solve(h_function)

        elif method == 'A*':
            self.a_star_solve(h_function)

        else:
            raise NameError('Unused method, please choose `BnB` or `A*`.')

        return reconstruct_solution(self.solution)

    def bnb_solve(self, h_function):

        # Init params
        solution = None
        open_list = [self.init_state]
        close_list = set()
        ub = 31
        iterations = 0

        while len(open_list) > 0:

            # Current node and current children of the node
            current_node = open_list.pop(0)
            current_children = []

            # Iteration status
            iterations += 1
            if iterations % 100 == 0:
                print('-- Status --')
                print('Open List: {}, Close List: {}, Iterations: {}'.format(len(open_list), len(close_list), iterations))
                print('Depth: {}, UB: {}'.format(current_node.depth(), ub))

            # For each available children
            for n in current_node.expand():

                # If this children is the goal state
                if (n == self.goal_state).all():

                    # If this solution is better then the current solution
                    if current_node.g_value + 1 < ub:
                        ub = current_node.g_value + 1
                        solution = Node(n, ub, ub, current_node)

                # This children is not the goal state
                else:

                    if n not in (set(open_list) | close_list):

                        lb = current_node.g_value + 1 + h_function(n, self.goal_state)
                        child_node = Node(n, current_node.g_value + 1, lb, current_node)

                        if lb < ub:
                            current_children.append(child_node)
                        else:  # todo: think if needed
                            close_list.append(child_node)

            current_children.sort(key=lambda x: x.lb)
            open_list = current_children + open_list
            # open_list.sort(key=lambda x: x.lb)
            close_list.append(current_node)

        self.solution = solution

    def a_star_solve(self, h_function):
        pass
