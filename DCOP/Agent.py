import numpy as np
import pickle
from .Message import Message
from typing import List, Dict, Any
from .Mailer import Mailer


class Agent:
    """
    A class representing an agent in a distributed environment

    Attributes
    ----------

    agent_id: int
        the id of the agent

    constraints: dict
        the constraints of the agent, as a dict, where neighbor is the key and the value is cost
        matrix as numpy ndarray.

    domain: list
        the list with the domain of the agent, each value is a int

    value: int
        the value from the domain which the agent selected as the current assignment

    """

    def __init__(self, agent_id, constraints, domain):

        self.id = agent_id  # type: int
        self.constraints = constraints  # type: Dict[int, np.array]
        self.domain = domain  # type: List[int]
        self.value = np.random.choice(domain)  # type: int

    def compute_cost(self, value: int, neighbors_values: Dict[int, int]) -> float:
        """
        The method compute the cost the agent pay according to a given value
        and a given neighbors' values
        :param neighbors_values: dict with the neighbors values in the form {neighbor: value}
        :param value: the value of the agent
        :return: cost as float
        """

        value_cost = 0

        # How much it will cost given my neighbor values
        for neighbor, neighbor_value in neighbors_values.items():

            value_cost += self.constraints[neighbor][value][neighbor_value]

        return value_cost

    def send_message(self, mailer: Mailer, content: Any):
        """
        The method gets a mailer and content and send the content to all
        the agent neighbors.
        :param content: content to send the neighbors
        :param mailer: mailer to use in order to send the messages
        :return:
        """

        for neighbor in self.constraints.keys():

            mailer.deliver_message(self.id, neighbor, content)

    def get_neighbors(self):

        return list(self.constraints.keys())