from tqdm import tqdm

from DCOP.Mailer import Mailer
from DCOP.DSA import DSA
from DCOP.Agent import Agent
from examples.generate_constraint import generate_constraints
import yaml
import pickle
from typing import List, Dict
import os
from pathlib import Path
import matplotlib.pyplot as plt

# Project root directory
root_directory = Path(__file__).parent.parent


def init_agents(mailer: Mailer, config):
    """

    :param mailer:
    :param config:
    :return:
    """

    agents_type = config['environment']['agents_type']
    n_agents = config['environment']['n_agents']
    domain = range(config['environment']['n_domain'])
    constraint_filename = config['constraints']['filename']['constraints']
    agents = []

    # Init agents according to the agent type
    if agents_type.lower() == 'dsa':

        for i in range(n_agents):

            # Init DSA params
            constraint_path = os.path.join(root_directory, constraint_filename)
            constraints = pickle.load(open(constraint_path.format(i), 'rb'))
            dsa_type = config['DSA']['type']
            p = config['DSA']['p']

            # Create agent and send value to neighbors
            a = DSA(i, constraints, domain, dsa_type, p)
            a.send_message(mailer, a.value)

            # Append the agent
            agents.append(a)

    elif agents_type.lower() == 'mgm2':

        raise NotImplementedError('MGM2 init agents')

    return agents


def compute_total_cost(agents: List[Agent]):
    """

    :return:
    """

    total_cost = 0

    # Debug - print all agents values
    # print({a.id: a.value for a in agents})

    for a in agents:

        neighbors_values = {}

        for n in a.get_neighbors():

            neighbors_values[n] = agents[n].value

        total_cost += a.compute_cost(a.value, neighbors_values)

    # todo: think if we need to divide it by 2
    return total_cost


def plot_cost(total_cost):

    plt.plot(total_cost)
    plt.show()


def main():

    # Load configuration file
    config_path = os.path.join(root_directory, 'DCOP/config.yaml')
    config = yaml.full_load(open(config_path))

    # If we don't have constraints generate them
    generate_constraints(config)

    # Init params
    mailer = Mailer()
    agents = init_agents(mailer, config)
    n_iteration = config['environment']['n_iteration']
    total_cost = []

    # Solve
    for i in tqdm(range(n_iteration)):

        # Move messages to inbox
        mailer.assign_messages()

        # Run each agent iteration
        for a in agents:

            a.iteration(mailer)

        # Update total cost
        total_cost.append(compute_total_cost(agents))

    # Plot cost
    plot_cost(total_cost)


if __name__ == '__main__':

    main()