import numpy as np
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
        the constraints of the agent as a dict, where neighbor is the key and the value is cost
        matrix as numpy ndarray.

    domain: list
        the list with the domain of the agent, each value is a int

    value: int
        the value from the domain which the agent selected as the current assignment

    """

    def __init__(self, agent_id, constraints, domain):

        self.id: int = agent_id
        self._constraints: Dict[int, np.array] = constraints
        self._domain: List[int] = domain
        self.value: int = np.random.choice(domain)
        self._neighbors: List[int] = list(self._constraints.keys())
        self._cost: int = np.inf

    def compute_cost(self, value: int, agents_values: Dict[int, int]) -> float:
        """
        The method compute the cost the agent pay according to a given value
        and a given other agents' values
        :param agents_values: dict with the agents values in the form {agent: value}
        :param value: the value of the agent
        :return: cost as float
        """

        value_cost = 0

        # Find the cost for each neighbor
        for n in self._neighbors:

            # Get the neighbor value from the `agents_values` arg
            try:
                neighbor_value = agents_values[n]
            except KeyError:
                raise KeyError('The neighbor {} is missing from the agents` values dict'.format(n))

            # Update the current cost
            value_cost += self._constraints[n][value][neighbor_value]

        return value_cost

    def send_value_messages(self, mailer: Mailer):
        """
        The method gets a mailer and content and send the content to all
        the agent neighbors.
        :param mailer: mailer to use in order to send the value messages
        :return:
        """

        for neighbor in self._constraints.keys():

            mailer.deliver_message(self.id, neighbor, self.value, 'value')

    @staticmethod
    def agent_cost(value: int, neighbors_values: Dict[int, int],
                   constraints: Dict[int, np.array]) -> float:

        """
        Compute a cost for a given agent's attributes
        :param value: the current value of the agent
        :param neighbors_values: dict with all the agent's neighbors values
        :param constraints: the constraints of the agents
        :return: the current cost
        """

        cost = 0

        # Find the cost for each neighbor
        for neighbor, neighbor_value in neighbors_values.items():

            # Update the cost
            cost += constraints[neighbor][value][neighbor_value]

        return cost

    @property
    def cost(self):
        # return 'Dont touch my cost'
        return self._cost
