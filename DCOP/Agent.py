import numpy as np
import pickle
from .Message import Message
from typing import List, Dict


class Agent:

    def __init__(self, agent_id, constraints, domain):

        self.id = agent_id  # type: int
        self.constraints = constraints  # type: Dict[int, np.array]
        self.domain = domain  # type: List[int]
        self.value = np.random.choice(domain)  # type: int

    def compute_cost(self, value: int, messages: List[Message]) -> float:
        """

        :param value:
        :param messages:
        :return:
        """

        value_cost = 0

        # How much it will cost given my neighbor values
        for m in messages:

            neighbor = m.sender
            neighbor_value = m.content

            value_cost += self.constraints[neighbor][value][neighbor_value]

        return value_cost
