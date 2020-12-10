import copy
import numpy as np
from .Node import Node
import time


def is_node_exist(table, open_set, parent):
    """
    This function get two lists and return if the table is in on of those lists
    :param table: ndarray represent the table
    :param open_list: list with the existed nodes
    :return: bool answer if the table appear in the existed list
    """

    # Check if this table already exist in open list
    if tuple(table.flatten()) in open_set:
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

    def solve(self, algorithm, h_function):
        """
        This method get an algorithm name to solve the eight-puzzle, and heuristic function.
        The method return a solution.
        :param algorithm: str, algorithm name
        :param h_function: function which get current table (matrix) and goal state (matrix)
                            and return scalar
        :return: solution as Node object
        """

        print('Using {} to solve the 8-puzzle...'.format(algorithm))
        print('Init table: \n{}'.format(self.init_state))

        if algorithm == 'BnB':
            self.bnb_solve(h_function)

        elif algorithm == 'A*':
            self.a_star_solve(h_function)

        else:
            raise NameError('Unused algorithm, please choose `BnB` or `A*`.')

        return reconstruct_solution(self.solution)

    def bnb_solve(self, h_function):

        # Init params
        solution = None
        open_list = [self.init_state]
        open_set = {tuple(self.init_state.table.flatten())}
        ub = np.inf
        iterations = 0

        while len(open_list) > 0:

            # Get the current parent node for this iteration
            parent = open_list.pop(0)
            open_set.remove(tuple(parent.table.flatten()))
            current_children = []

            # todo: need just close set
            parent_depth = parent.depth()

            # Iteration status
            iterations += 1
            if iterations % 100 == 0:
                print('---- Status ----')
                print('Open List: {}, Iterations: {}, UB: {}'.format(len(open_list), iterations, ub))

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
                    if not is_node_exist(child, open_set, parent):

                        lb = parent_depth + 1 + h_function(child, self.goal_state)

                        if lb < ub:
                            current_children.append(Node(child, lb, parent))

            # Update open list with the relevant children
            open_list = current_children + open_list
            open_list.sort(key=lambda x: x.lb)

            # Update open set
            for c in current_children:
                open_set.add(tuple(c.table.flatten()))

        self.solution = solution

    def a_star_solve(self, h_function):
        pass

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
