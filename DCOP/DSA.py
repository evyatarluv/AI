from .Agent import Agent
from .Mailer import Mailer
from .Message import Message
from typing import List, Dict
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

    def iteration(self, mailer: Mailer):
        """

        :param mailer:
        :return:
        """

        # Get the current messages as neighbors' values
        neighbors_values = {m.sender: m.content for m in mailer.get_messages(self.id)}

        # Find the current best value
        new_value = self.find_best_value(neighbors_values)

        # Choose if to replace the current value
        if self.replacement_decision(new_value, neighbors_values):

            self.value = new_value

        # Send the current value
        self.send_message(mailer, self.value)

    def find_best_value(self, neighbors_values: Dict[int, int]) -> int:
        """
        The method compute the best current value according to the neighbors' values
        :param neighbors_values: dict with the neighbors values as {neighbor: value}
        :return: best possible value as int
        """

        costs = dict()

        # For each value in the domain find current cost
        for value in self.domain:

            if value != self.value:

                costs[value] = self.compute_cost(value, neighbors_values)

        # Return the value which has the minimum cost
        return min(costs, key=costs.get)

    def replacement_decision(self, new_value: int, neighbors_values: Dict[int, int]):
        """
        The method decide if to replace the agent's value or to stay with the current value.
        :param new_value: value the agent want to change to
        :param neighbors_values: the current values of the agent's neighbors
        :return: bool answer, replace or not
        """

        new_cost = self.compute_cost(new_value, neighbors_values)
        current_cost = self.compute_cost(self.value, neighbors_values)

        # Choose the replacement decision according to DSA type
        # C - new cost better or equal
        if self.type.lower() == 'c':
            if new_cost <= current_cost:

                if np.random.random() < self.p:

                    return True

            return False

        # todo: Add other DSA types, i.e., A, B, ....








