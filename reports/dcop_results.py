from tqdm import tqdm
from DCOP.MGM2 import MGM2
from DCOP.Mailer import Mailer
from DCOP.DSA import DSA
from DCOP.Agent import Agent
from DCOP.generate_constraints import generate_constraints
import yaml
import pickle
from typing import List, Dict
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Project root directory
root_directory = Path(__file__).parent.parent

# Results params
n_runs = 10
p1 = 0.5
p2_values = np.arange(0.1, 1, 0.1)


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


def compare_p2():

    results = {}  # in the form of { val_1: [run_1, run_2, ...., ], ... }

    for p2 in p2_values:

        # Verbose
        print('p2 = {}'.format(p2))

        # Load configuration file
        config_path = os.path.join(root_directory, 'DCOP/config.yaml')
        config = yaml.full_load(open(config_path))
        config['constraints']['problem_toughness'] = p2  # update p2
        config['constraints']['problem_density'] = p1  # update p1

        # Init results list for the current p2 value
        results[p2] = []

        # Run it n_runs times
        for i in range(n_runs):

            # Update seed
            config['constraints']['seed'] += i

            # Generate constraints
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
                total_cost.append(sum([a.cost for a in agents]))

            # Update the results
            results[p2].append(total_cost[-1])

    filename = 'results/compare_p2/p1_{}/{}.pickle'.format(str(p1).replace('.', ''),
                                                           config['environment']['agents_type'])
    pickle.dump(results, open(filename, 'wb'))


def compare_iterations():

    results = {}  # in the form of { run_1: [iter_1, iter_2, .... ] }

    # Load configuration file
    config_path = os.path.join(root_directory, 'DCOP/config.yaml')
    config = yaml.full_load(open(config_path))
    config['constraints']['problem_density'] = p1  # update p1

    # Run it n_runs times
    for i in range(n_runs):

        # Update seed
        config['constraints']['seed'] += i

        # Generate constraints
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
            total_cost.append(sum([a.cost for a in agents]))

        # Update the results
        results[i] = total_cost

    filename = 'results/compare_iterations/p1_{}/{}.pickle'.format(str(p1).replace('.', ''),
                                                             config['environment']['agents_type'])
    pickle.dump(results, open(filename, 'wb'))


if __name__ == '__main__':

    # compare_p2()
    
    compare_iterations()
