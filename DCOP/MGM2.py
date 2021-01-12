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
            the domain of the bidder.
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

    Attributes:
    ----------

    todo: add attributes explanation

    """

    def __init__(self, agent_id, constraints, domain, offer_prob):

        super(MGM2, self).__init__(agent_id, constraints, domain)

        self._iteration_count: int = 1
        self._neighbors_values: Dict[int, int] = {}
        self._committed: bool = False
        self._offer_prob: float = offer_prob
        self._partner = None
        self._new_value = None
        self._gain = None
        self._change_value = None
        self._iteration_switcher: Dict[int, Callable] = {1: self._commit_offers,
                                                         2: self._response_offers,
                                                         3: self._send_gain,
                                                         4: self._find_max_gain,
                                                         5: self._update_new_value,
                                                         }

    def iteration(self, mailer: Mailer):

        # Execute iteration according to the counter
        self._iteration_switcher[self._iteration_count](mailer)

        # Update iteration counter
        self._iteration_count = (self._iteration_count + 1) if self._iteration_count < 5 else 1

    def _commit_offers(self, mailer: Mailer):
        """
        Method for iteration #1.

        The agent does the following steps:

            1. Get his neighbors' values (using the messages from the last step)

            2. Decide if to send an offer.

        :param mailer: mailer for getting and sending messages
        :return:
        """

        # Get the current messages as neighbors' values
        self._neighbors_values = {m.sender: m.content for m in mailer.get_messages(self.id)}

        # Override partner, gain and new_value from last cycle
        self._partner = None
        self._update_gain()

        # Decide to offer or not
        if np.random.random() < self._offer_prob:

            self._committed = True

            # Choose partner
            partner = np.random.choice(self._neighbors)

            # Create & send the offer
            offer = Offer(self._neighbors_values, self._constraints, self.value, self._domain)
            mailer.deliver_message(self.id, partner, offer, 'Offer')

        else:

            self._committed = False

    def _response_offers(self, mailer: Mailer):
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
                mailer.deliver_message(self.id, sender, response, 'Response')

        # If the agent didn't committed an offer -
        # choose the best offer and response with `yes`
        else:
            # If the agent got offers choose the best one
            if offers:

                # Find the best value and update attributes
                partner_value = self._find_best_offer(offers)

                # Accept the best offer reject all others
                for sender in offers.keys():

                    # Create the response message according the sender
                    if sender == self._partner:

                        response = Response(accept=True, gain=self._gain, value=partner_value)

                    else:

                        response = Response(accept=False)

                    # Send the message
                    mailer.deliver_message(self.id, sender, response, 'Response')

    def _send_gain(self, mailer: Mailer):
        """
        Method for iteration #3.

        The agent does the following steps:

            1. If the agent committed an offer and received a `accept` response then update
                the partner gain and new value according the response message

            2. Send the agent's gain to all his neighbors except the partner (if there is one)

        :param mailer: mailer for getting and sending messages
        :return:
        """

        # If an offer was committed - look for your response
        if self._committed:

            # Unpack the response from the message
            sender: int = mailer.get_messages(self.id)[0].sender
            response: Response = mailer.get_messages(self.id)[0].content

            # If the partner accept my offer
            if response.accept:

                # Update attributes
                self._partner = sender
                self._gain = response.gain
                self._new_value = response.value

        # Send the gain to all neighbors except the partner
        for neighbor in self._neighbors:

            if neighbor != self._partner:

                mailer.deliver_message(self.id, neighbor, self._gain, 'Gain')

    def _find_max_gain(self, mailer: Mailer):
        """
        Method for iteration #4.

        The agent does the following steps:

            1. Check if the agent got the maximum gain.

            2. Update according to step 1 the change_value attribute and send to the partner (if there
                is one)

        :param mailer: mailer for getting and sending messages
        :return:
        """

        neighbors_gain: Dict[int, float] = {m.sender: m.content for m in mailer.get_messages(self.id)}

        # Assert if length dont match what excepted
        if self._partner is not None:
            assert len(neighbors_gain) == len(self._neighbors) - 1
        else:
            assert len(neighbors_gain) == len(self._neighbors)

        # If my gain is the maximum gain
        if (self._gain > max(neighbors_gain.values())) & (self._gain > 0):

            self._change_value = True

        else:

            self._change_value = False

        # If I got a partner - update him
        if self._partner is not None:

            mailer.deliver_message(self.id, self._partner, self._change_value, 'Change Value')

    def _update_new_value(self, mailer: Mailer):
        """
        iteration #5
        todo: docstring
        :param mailer:
        :return:
        """

        # If the agent dont have value (lonely wolf according to Zohar)
        if self._partner is None:

            if self._change_value:

                self.value = self._new_value

        # The agent have a partner
        else:

            partner_change = mailer.get_messages(self.id)[0].content

            if partner_change & self._change_value:

                self.value = self._new_value

        self.send_value_messages(mailer)

    def _find_best_offer(self, offers: Dict[int, Offer]) -> int:
        """
        The method get a dict of offers as { agent_id: Offer } and find the best offer.

        For each offer and sender the method runs over all the values combination and find the
        best combination (the one with the lowest cost). For the lowest cost the method computes
        the corresponding gain and the gain and the values which lead to this gain.

        Next, the method find the best gain and update the partner, the new value and the shared gain.

        The method returns the partner's value in order to send it to the partner as a message.
        :param offers: dict with all the offers as value and bidder as key.
        :return: partner's values, int
        """

        # Init gains dict with the form of:
        # { bidder_id: {self_value: int, partner_value: int, gain: float} }
        gains: Dict[int, Dict] = {}

        # For each offer find the best new values for both of us
        # Then save these values and the new cost
        for sender, o in offers.items():

            # Compute current cost
            current_cost = MGM2.compute_pair_cost(
                agent_1=(self.id, self.value, self._neighbors_values, self._constraints),
                agent_2=(sender, o.value, o.neighbors_values, o.constraints))  # best cost as current cost

            # Look for the best cost and values
            best_cost = current_cost
            best_values = (self.value, o.value)  # tuple as (my_value, partner_value)

            # For each combination of assignments
            for self_value, partner_value in product(self._domain, o.domain):

                # Update current self neighbors values
                self_neighbors_values = deepcopy(self._neighbors_values)
                self_neighbors_values[sender] = partner_value

                # Update current partner neighbors values
                partner_neighbors_values = deepcopy(o.neighbors_values)
                partner_neighbors_values[self.id] = self_value

                # Compute new cost
                new_cost = MGM2.compute_pair_cost(
                    agent_1=(self.id, self_value, self_neighbors_values, self._constraints),
                    agent_2=(sender, partner_value, partner_neighbors_values, o.constraints)
                )

                # Update best cost and values
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_values = (self_value, partner_value)

            # Update the best gain corresponding to the sender
            gains[sender] = {'self_value': best_values[0], 'partner_value': best_values[1],
                             'gain': current_cost - best_cost}

        # Get the best partner corresponding to the max gain
        best_partner = max(gains, key=lambda x: gains.get(x)['gain'])

        # Update partner, gain and new value
        self._partner = best_partner
        self._gain = gains[best_partner]['gain']
        self._new_value = gains[best_partner]['self_value']

        # Return the partner new value
        return gains[best_partner]['partner_value']

    def _update_gain(self):
        """
        The method find the best new value and the corresponding gain.
        The method update these attributes.
        :return:
        """

        gains = dict()
        current_cost = self.compute_cost(self.value, self._neighbors_values)

        # For each value in the domain find current gain
        for value in self._domain:

            gains[value] = self.compute_cost(value, self._neighbors_values) - current_cost

        # Find the value with the max gain and update it
        self._new_value = max(gains, key=gains.get)
        self._gain = gains[self._new_value]

    @staticmethod
    def compute_pair_cost(agent_1: Tuple, agent_2: Tuple):
        """
        Compute the cost for pair of agents.

        Each agent consist of the following tuple:
            (id, value, neighbors_values, constraints)

        :param agent_1: first agent from the pair
        :param agent_2: second agent from the pair
        :return: cost of the pair
        """

        # Unpacking agents
        self_id, self_value, self_neighbors_values, self_constraints = agent_1
        partner_id, partner_value, partner_neighbors_values, partner_constraints = agent_2

        # Compute costs
        self_cost = Agent.agent_cost(self_value, self_neighbors_values, self_constraints)
        partner_cost = Agent.agent_cost(partner_value, partner_neighbors_values, partner_constraints)
        join_cost = self_constraints[partner_id][self_value][partner_value]

        return partner_cost + self_cost - join_cost







