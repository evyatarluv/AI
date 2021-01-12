from tqdm import tqdm
from DCOP.MGM2 import MGM2
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
    n_iteration = config['environment']['n_iteration']
    agents = []

    # Create agents
    for i in range(n_agents):

        # Load agent's constraints
        constraint_path = os.path.join(root_directory, constraint_filename)
        constraints = pickle.load(open(constraint_path.format(i), 'rb'))

        # Init agents according to the agent type
        if agents_type.lower() == 'dsa':

            # Init DSA params
            dsa_type = config['DSA']['type']
            p = config['DSA']['p']

            # Create agent and send value to neighbors
            a = DSA(i, constraints, domain, dsa_type, p)

        elif agents_type.lower() == 'mgm2':

            # Init MGM2 params
            # todo: think of something wiser
            n_iteration = config['MGM2']['iterations_in_cycle'] * config['environment']['n_iteration']
            offer_prob = config['MGM2']['offer_probability']

            # Create agent
            a = MGM2(i, constraints, domain, offer_prob)

        else:
            raise NotImplementedError('Not implemented agent type')

        # Send value to neighbors & append the agent
        a.send_value_messages(mailer)
        agents.append(a)

    return agents, n_iteration


def compute_total_cost(agents: List[Agent]):
    """

    :return:
    """

    total_cost = 0
    agents_values = {a.id: a.value for a in agents}

    for a in agents:
        total_cost += a.compute_cost(a.value, agents_values)

    return total_cost


def plot_cost(total_cost, config):

    agent_type = config['environment']['agents_type']
    # todo: read cycle from config

    if agent_type.lower() == 'mgm2':
        total_cost = [total_cost[i] for i in range(5, len(total_cost), 5)]

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
    agents, n_iterations = init_agents(mailer, config)
    total_cost = []

    # Solve
    for _ in tqdm(range(n_iterations)):

        # Move messages to inbox
        mailer.assign_messages()

        # Run each agent iteration
        for a in agents:
            a.iteration(mailer)

        # Update total cost
        total_cost.append(compute_total_cost(agents))

    # Plot cost
    plot_cost(total_cost, config)


if __name__ == '__main__':
    main()
