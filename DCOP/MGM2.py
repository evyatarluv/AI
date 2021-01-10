from .Agent import Agent
from .Mailer import Mailer
import numpy as np
from typing import List, Dict, Callable, Any


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

    """
    def __init__(self, neighbors_values, constraints, value):
        self.neighbors_values: Dict[int, int] = neighbors_values
        self.constraints: Dict[int, np.array] = constraints
        self.value: int = value


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
            offer = Offer(self._neighbors_values, self._constraints, self.value)
            mailer.deliver_message(self.id, neighbor, offer, 'offer')

        else:

            self.committed = False

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
            best_neighbor, gain, value = self._find_best_offer(offers)

            # Accept the best offer reject all others
            for sender in offers.keys():

                # Create the response message according the sender
                if sender == best_neighbor:

                    response = Response(accept=True, gain=gain, value=value)

                else:

                    response = Response(accept=False)

                # Send the message
                mailer.deliver_message(self.id, sender, response, 'response')

    def _find_best_offer(self, offers: Dict[int, Offer]):

        # todo: fill this up
        pass
