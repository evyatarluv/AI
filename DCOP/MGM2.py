from .Agent import Agent
from .Mailer import Mailer
import numpy as np
from typing import List, Dict, Any


class MGM2(Agent):

    """
    A class representing an agent implementing MGM-2 algorithm
    """

    def __init__(self, agent_id, constraints, domain):

        super(MGM2, self).__init__(agent_id, constraints, domain)

        self.iteration_count: int = 1
        # todo: MGM2 other attributes

    def iteration(self):

        pass

