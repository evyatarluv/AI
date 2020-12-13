"""
Script for all the heuristics functions
"""

import numpy as np


def h_manhattan(table, goal_table):
        """
        This h function calculate the sum of manhattan distance between current table
        to the goal table.
        :param table: current table, ndarray with shape (3,3)
        :param goal_table: gaol state table, ndarray with shape (3,3)
        :return:
        """

        manhattan_sum = 0

        for i in range(1, 9):
            # Get position on current table
            table_pos = np.where(table == i)

            # Get position on goal table
            goal_pos = np.where(goal_table == i)

            # Compute manhattan distance and sum
            x_distance = np.abs(table_pos[0][0] - goal_pos[0][0])
            y_distance = np.abs(table_pos[1][0] - goal_pos[1][0])
            manhattan_sum += x_distance + y_distance

        return manhattan_sum


def h_misplaced(table, goal_table):
        """
        h function which count the number of misplaced number in a given state
        :param table: current state, ndarray
        :param goal_table: goal state, ndarray
        :return: number of misplaced, int
        """

        # Flat both tables and change to list
        goal_table = list(goal_table.flatten())
        table = list(table.flatten())

        misplaced = 0

        for i in range(1, 9):
            # if the i number is misplaced
            if goal_table.index(i) != table.index(i):
                misplaced += 1

        return misplaced