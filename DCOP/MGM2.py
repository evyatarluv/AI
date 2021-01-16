from .Agent import Agent
from .Mailer import Mailer
from .Message import Message
import numpy as np
from typing import List, Dict, Callable, Tuple
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

    todo: add attributes' explanation

    """
    # todo: Roie told in the lecture that in MGM2 in every iteration all agents must send messages
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
                                                         5: self._update_new_value}

    def iteration(self, mailer: Mailer):

        # Execute iteration according to the counter
        self._iteration_switcher[self._iteration_count](mailer)

        # Update iteration counter
        self._iteration_count = (self._iteration_count + 1) if self._iteration_count < 5 else 1

    # Iteration 1
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

        # Update cost
        self._cost = self.compute_cost(self.value, self._neighbors_values)

        # Override partner, gain and new_value from last cycle
        self._partner = None
        self._update_gain()

        # Decide to offer or not
        partner = None
        if (np.random.random() < self._offer_prob) and self._neighbors:

            self._committed = True
            partner = np.random.choice(self._neighbors)

        else:

            self._committed = False

        # Send messages to neighbors
        for neighbor in self._neighbors:

            if neighbor == partner:
                msg = Offer(self._neighbors_values, self._constraints, self.value, self._domain)

            else:
                msg = None

            # Send the message
            mailer.deliver_message(self.id, neighbor, msg, 'Offer')

    # Iteration 2
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
        offers: Dict[int, Offer] = {m.sender: m.content
                                    for m in mailer.get_messages(self.id) if m.content is not None}

        # Get best offer (if so)
        partner_value = self._find_best_offer(offers)

        for neighbor in self._neighbors:

            if neighbor == self._partner:
                msg = Response(accept=True, gain=self._gain, value=partner_value)

            elif neighbor in offers.keys():
                msg = Response(accept=False)

            else:
                msg = None

            mailer.deliver_message(self.id, neighbor, msg, 'Response')

    # Iteration 3
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

        # Get response
        msg: List[Message] = [m for m in mailer.get_messages(self.id) if m.content is not None]

        # If an offer was committed - look for your response
        if self._committed:

            # Unpack the response from the message
            sender: int = msg[0].sender
            response: Response = msg[0].content

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

    # Iteration 4
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
        if self._is_max_gain(neighbors_gain) & (self._gain > 0):

            self._change_value = True

        else:

            self._change_value = False

        # Send messages to neighbors
        # To the partner send the `change_value` attribute
        for neighbor in self._neighbors:

            if neighbor == self._partner:
                msg = self._change_value

            else:
                msg = None

            mailer.deliver_message(self.id, self._partner, msg, 'Change Value')

    # Iteration 5
    def _update_new_value(self, mailer: Mailer):
        """
        Method for iteration #5.

        The agent does the following steps:

            1. If the agent have no partner and have max gain - change value

            2. If the agent have partner and both of them got max gain - change value

            3. For any other option the agent stay with his old value

        :param mailer: mailer for getting and sending messages
        :return:
        """
        # Get messages
        msg: List[Message] = [m for m in mailer.get_messages(self.id) if m.content is not None]

        # If the agent dont have partner (lonely wolf according to Zohar)
        if self._partner is None:

            if self._change_value:

                self.value = self._new_value

        # The agent have a partner
        else:

            partner_change = msg[0].content

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

        # todo
        if (len(offers) == 0) | self._committed:
            return -1

        # Init gains dict with the form of:
        # { bidder_id: {self_value: int, partner_value: int, gain: float} }
        gains: Dict[int, Dict] = {}

        # For each offer find the best new values for both of us
        # Then save these values and the new cost
        for sender, o in offers.items():

            # Compute current cost
            current_cost = MGM2.compute_pair_cost(
                agent_1=(self.id, self.value, self._neighbors_values, self._constraints),
                agent_2=(sender, o.value, o.neighbors_values, o.constraints))

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
                    agent_2=(sender, partner_value, partner_neighbors_values, o.constraints))

                # Update best cost and values
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_values = (self_value, partner_value)

            # Update the best gain corresponding to the sender
            gains[sender] = {'self_value': best_values[0], 'partner_value': best_values[1],
                             'gain': current_cost - best_cost}

        # Get the best partner corresponding to the max gain
        self._partner = max(gains, key=lambda x: gains.get(x)['gain'])

        # Update partner, gain and new value
        self._new_value, partner_value, self._gain = gains[self._partner].values()

        # Return the partner new value
        return partner_value

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

            gains[value] = current_cost - self.compute_cost(value, self._neighbors_values)

        # Find the value with the max gain and update it
        self._new_value = max(gains, key=gains.get)
        self._gain = gains[self._new_value]

    def _is_max_gain(self, neighbors_gain: Dict[int, float]) -> bool:
        """
        The method check if the agent have max gain relative to his neighbors.

        The method uses the neighbors_gain dict to compare the gains. The gain of the agent's
        partner (if so) was already removed from the dict.

        Note:
        ----
        In case of equality between gain - tiebreaker with index (the agent with the bigger
        index win)

        :param neighbors_gain: dict with the neighbors' gain while each key is the neighbor id
                                and the value is the neighbor's gain.
        :return: bool answer, True for max and False otherwise.
        """

        for neighbor, gain in neighbors_gain.items():

            if self._gain < gain:

                return False

            elif (self._gain == gain) & (self.id < neighbor):

                return False

        return True

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








