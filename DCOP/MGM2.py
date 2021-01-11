from .Agent import Agent
from .Mailer import Mailer
import numpy as np
from typing import List, Dict, Callable, Any, Tuple
from itertools import product
from copy import deepcopy

class Offer:
    """
    Class for representing an offer of one agent to another

    Attributes:
    ----------

        neighbors_values: (dict)
            the values of the bidder's neighbors as a dict where each neighbor is a key and the neighbor's
            value as a value.

        constraints: (dict)
            the constraints of the bidder, where each neighbor is a key and the matrix cost as a value.

        value: (int)
            the current value of the bidder.

        domain: (List[int])
            # todo: explain
    """
    def __init__(self, neighbors_values, constraints, value, domain):
        self.neighbors_values: Dict[int, int] = deepcopy(neighbors_values)
        self.constraints: Dict[int, np.array] = deepcopy(constraints)
        self.value: int = value
        self.domain: List[int] = deepcopy(domain)


class Response:
    """
    Class representing a response for an offer.

    Attributes:
    ----------

        accept: (bool)
            True for accept the offer and False for reject it.

        gain: (float)
            the gain for changing from the current bidder's value to the new value

        value: (int)
            the value of bidder that the responder compute as the best new value


    """
    def __init__(self, accept, gain=None, value=None):

        self.accept = accept

        if accept:
            if (value is None) or (gain is None):
                raise ValueError(
                    'If you send an accept message, you must send the neighbor'
                    'value and the global gain in it too'
                )

        self.value: int = value
        self.gain: float = gain


class MGM2(Agent):
    """
    A class representing an agent implementing MGM-2 algorithm
    """

    def __init__(self, agent_id, constraints, domain, offer_prob):

        super(MGM2, self).__init__(agent_id, constraints, domain)

        self._iteration_count: int = 1
        self._neighbors_values: Dict[int, int] = {}
        self._committed: bool = False
        self._offer_prob: float = offer_prob
        self._iteration_switcher: Dict[int, Callable] = {1: self._commit_offers,
                                                         2: self._create_pairs,
                                                         3: None,
                                                         4: None,
                                                         5: None,
                                                         }

    def iteration(self, mailer: Mailer):

        # Execute iteration according to the counter
        self._iteration_switcher[self._iteration_count](mailer)

        # Update iteration counter
        self._iteration_count += 1 if self._iteration_count < 5 else 1

    def _commit_offers(self, mailer: Mailer):
        """
        Method for iteration #1.

        The agent does the following steps:

            1. Get his neighbors' values (using the messages from the last step)

            2. Decide if to send an offer, if decide true - send an offer.

        :param mailer: mailer for getting and sending messages
        :return:
        """
        # Get the current messages as neighbors' values
        self._neighbors_values = {m.sender: m.content for m in mailer.get_messages(self.id)}

        # Decide to offer or not
        if np.random.random() < self._offer_prob:

            self._committed = True

            # Choose neighbor
            neighbor = np.random.choice(self._neighbors)

            # Create & send the offer
            offer = Offer(self._neighbors_values, self._constraints, self.value, self._domain)
            mailer.deliver_message(self.id, neighbor, offer, 'offer')

        else:

            self._committed = False

    # todo: change the method name
    def _create_pairs(self, mailer: Mailer):
        """
        Method for iteration #2.

        The agent does the following steps:

            1. Get the received offers (using the messages from the last step)

            2. Answer to the offers according the `committed` attribute from last step.

        :param mailer: mailer for getting and sending messages
        :return:
        """
        # Get all offers
        offers: Dict[int, Offer] = {m.sender: m.content for m in mailer.get_messages(self.id)}

        # If the agent committed an offer -
        # answer `no` to all offers
        if self._committed:

            # Create the response message
            response = Response(accept=False)

            for sender in offers.keys():
                mailer.deliver_message(self.id, sender, response, 'response')

        # If the agent didn't committed an offer -
        # choose the best offer and response with `yes`
        else:

            # Get the neighbor, gain & value which corresponded to the best offer
            self_value, partner, partner_value, gain = self._find_best_offer(offers)

            # Accept the best offer reject all others
            for sender in offers.keys():

                # Create the response message according the sender
                if sender == partner:

                    response = Response(accept=True, gain=gain, value=partner_value)

                else:

                    response = Response(accept=False)

                # Send the message
                mailer.deliver_message(self.id, sender, response, 'response')

    def _find_best_offer(self, offers: Dict[int, Offer]):

        gains: Dict[int, Tuple] = {}

        for sender, o in offers.items():

            current_cost = MGM2.compute_pair_cost(
                agent_1=(self.id, self.value, self._neighbors_values, self._constraints),
                agent_2=(sender, o.value, o.neighbors_values, o.constraints)
            )

            costs: Dict[Tuple: float] = {}

            for self_value, partner_value in product(self._domain, o.domain):

                # Update self neighbors values
                self_current_neighbors_values = deepcopy(self._neighbors_values)
                self_current_neighbors_values[sender] = partner_value

                # Update partner neighbors values
                partner_current_neighbors_values = deepcopy(o.neighbors_values)
                partner_current_neighbors_values[self.id] = self_value

                # Compute new cost
                new_cost = MGM2.compute_pair_cost(
                    agent_1=(self.id, self_value, self_current_neighbors_values, self._constraints),
                    agent_2=(sender, partner_value, partner_current_neighbors_values, o.constraints)
                )

                # Append the computed cost
                costs[(self_value, partner_value)] = new_cost

            # Get the assignments which lead to the best cost
            best_values = min(costs, key=costs.get)
            best_cost = costs[best_values]

            # Update the best gain corresponding to the sender
            gains[sender] = (best_values, current_cost - best_cost)

        # todo: return values
        return None, None, None, None

    @staticmethod
    def compute_pair_cost(agent_1: Tuple, agent_2: Tuple):

        """
        todo: docstring
        Each agent consist of the following tuple:
        (id, value, neighbors_values, constraints)
        :param agent_1:
        :param agent_2:
        :return:
        """

        # Unpacking agents
        self_id, self_value, self_neighbors_values, self_constraints = agent_1
        partner_id, partner_value, partner_neighbors_values, partner_constraints = agent_2

        # Compute costs
        partner_cost = Agent.agent_cost(partner_value, partner_neighbors_values, partner_constraints)
        self_cost = Agent.agent_cost(self_value, self_neighbors_values, self_constraints)
        join_cost = self_constraints[partner_id][self_value][partner_value]

        return partner_cost + self_cost - join_cost





