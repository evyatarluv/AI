

class Constraints:

    def __init__(self):

        self.constraints = {}

    def add_constraint(self, neighbor, costs):

        self.constraints[neighbor] = costs

    def get_costs(self, neighbor):

        return self.constraints[neighbor]