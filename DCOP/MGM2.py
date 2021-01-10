from .Agent import Agent
from .Mailer import Mailer
import numpy as np
from typing import List, Dict, Callable


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
                                                         2: None,
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

        # Get the current messages as neighbors' values
        self._neighbors_values = {m.sender: m.content for m in mailer.get_messages(self.id)}

        # Decide to offer or not
        if np.random.random() < self._offer_prob:

            self._committed = True

            # Choose neighbor and send offer
            neighbor = np.random.choice(self.neighbors)
            self._send_offer(mailer, neighbor)

        else:

            self.committed = False

    def _send_offer(self, mailer: Mailer, neighbor: int):

        # Create the offer message
        offer = {'neighbors_values': self._neighbors_values,
                 'constraints': self._constraints,
                 'value': self.value,
                 }

        # Send the offer to the neighbor
        mailer.deliver_message(self.id, neighbor, offer)
