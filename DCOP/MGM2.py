from .Agent import Agent
from .Mailer import Mailer
import numpy as np
from typing import List, Dict, Any


class MGM2(Agent):

    """
    A class representing an agent implementing MGM-2 algorithm
    """

    def __init__(self, agent_id, constraints, domain, offer_prob):

        super(MGM2, self).__init__(agent_id, constraints, domain)

        self.iteration_count: int = 1
        self.neighbors_values: Dict[int, int] = {}
        self.committed: bool = False
        self.offer_prob: float = offer_prob
        self.iteration_switcher = {1: self.commit_offers,
                                   2: None,
                                   3: None,
                                   4: None,
                                   5: None,
                                   }
        # todo: MGM2 other attributes

    def iteration(self, mailer: Mailer):

        # Execute iteration according to the counter
        self.iteration_switcher[self.iteration_count](mailer)

        # Update iteration counter
        self.iteration_count += 1 if self.iteration_count < 5 else 1

    def commit_offers(self, mailer: Mailer):

        # Get the current messages as neighbors' values
        self.neighbors_values = {m.sender: m.content for m in mailer.get_messages(self.id)}

        # Decide to offer or not
        if np.random.random() < self.offer_prob:

            self.committed = True

            # Choose neighbor and send offer
            neighbor = np.random.choice(self.neighbors, 1)
            self.send_offer(mailer, neighbor)

        else:

            self.committed = False

    def send_offer(self, mailer: Mailer, neighbor: int):

        # Create the offer message
        offer = {'neighbors_values': self.neighbors_values,
                 'constraints': self.constraints,
                 'value': self.value,
                 }

        # Send the offer to the neighbor
        mailer.deliver_message(self.id, neighbor, offer)

