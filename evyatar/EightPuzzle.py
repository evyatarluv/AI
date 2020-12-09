import copy
import numpy as np
from .Node import Node
import time


def is_node_exist(table, open_list, parent):
    """
    This function get two lists and return if the table is in on of those lists
    :param table: ndarray represent the table
    :param open_list: list with the existed nodes
    :return: bool answer if the table appear in the existed list
    """

    # Check if this table already exist in open list
    for t in open_list:
        if (t.table == table).all():
            return True

    # Look through all parents
    node = parent.parent
    while node is not None:

        if (table == node.table).all():
            return True
        else:
            node = node.parent

    return False


def reconstruct_solution(solution):

    solution_list = [solution]
    node = solution.parent

    while node is not None:

        solution_list.insert(0, node)
        node = node.parent

    return solution_list


class EightPuzzle:

    def __init__(self, init_state, goal_state):

        self.init_state = Node(init_state, 0, None)

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
        ub = 100
        iterations = 0

        while len(open_list) > 0:

            # Current node and current children of the node
            parent = open_list.pop(0)
            current_children = []

            # Iteration status
            iterations += 1
            if iterations % 100 == 0:
                print('-- Status --')
                print('Open List: {}, Iterations: {}'.format(len(open_list), iterations))
                print('Depth: {}, UB: {}'.format(parent.depth(), ub))

            # For each available children
            for child in parent.expand():

                # If this children is the goal state
                if (child == self.goal_state).all():

                    # If this solution is better then the current solution
                    steps = parent.depth() + 1
                    if steps < ub:
                        ub = steps
                        solution = Node(child, ub, parent)

                # This child is not the goal state
                else:
                    if not is_node_exist(child, open_list, parent):

                        g_value = parent.depth() + 1
                        lb = g_value + h_function(child, self.goal_state)
                        child_node = Node(child, lb, parent)

                        if lb < ub:
                            current_children.append(child_node)

            # Update open list with the relevant children
            current_children.sort(key=lambda x: x.lb)  # sort all children
            open_list = current_children + open_list
            # open_list.sort(key=lambda x: x.lb)

        self.solution = solution

    def a_star_solve(self, h_function):
        pass
