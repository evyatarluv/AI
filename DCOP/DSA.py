from .Agent import Agent
from .Message import Message
from typing import List
import numpy as np


class DSA(Agent):

    def __init__(self, agent_id, constraints, domain, dsa_type, p):

        super().__init__(agent_id, constraints, domain)
        self.p = p  # type: float

        # Init DSA type
        if dsa_type.lower() in ['c']:
            self.type = dsa_type  # type: str
        else:
            raise NotImplementedError('Not implemented DSA type')

    def iteration(self, messages: List[Message]):
        """

        :param messages:
        :return:
        """
        new_value = self.find_best_value(messages)

        if self.replacement_decision(new_value, messages):

            self.value = new_value

    def find_best_value(self, messages: List[Message]):
        """

        :param messages:
        :return:
        """

        costs = dict()

        # For each value in the domain find current cost
        for value in self.domain:

            if value != self.value:

                costs[value] = self.compute_cost(value, messages)

        return min(costs, key=costs.get)

    def replacement_decision(self, new_value, messages):
        """

        :param new_value:
        :param messages:
        :return:
        """

        new_cost = self.compute_cost(new_value, messages)
        current_cost = self.compute_cost(self.value, messages)

        # C - new cost better or equal
        if self.type.lower() == 'c':
            if new_cost <= current_cost:

                if np.random.random() < self.p:

                    return True

            return False

        # todo: Add other DSA types, i.e., A, B, ....








