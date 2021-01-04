"""

This script responsible for generating random constraint for DCOP.

"""
import yaml
from itertools import combinations
import numpy as np
import pickle

# todo: add documentation for functions

def generate_constraints_dict(vertex, config):

    """
    The function get list of tuples and for each tuple generate constraint matrix costs.
    :param config: configuration dict
    :param vertex: list of tuples
    :return: dict where each key is a tuple and the value is ndarray.
    """

    n_domain = config['environment']['n_domain']
    cost_range = config['constraints']['cost_range']
    constraints = {}

    for v in vertex:

        constraints[v] = np.random.randint(cost_range[0], cost_range[1], (n_domain, n_domain))

    return constraints


def export_constraints(constraints, config):
    """

    :param config:
    :param constraints:
    :return:
    """
    constraints_filename = config['constraints']['filename']
    n_agent = config['environment']['n_agents']
    agents_constraints = {a: {} for a in range(n_agent)}  # example: {agent: {other_agent: costs, ...}, ...}

    # Re-construct the dict by agents instead of tuples
    for variables, cost in constraints.items():

        agents_constraints[variables[0]][variables[1]] = cost
        agents_constraints[variables[1]][variables[0]] = cost

    # For each agent export the constraints dict
    for agent, costs in agents_constraints.items():

        pickle.dump(costs, open(constraints_filename.format(agent), 'wb'))


def choose_vertex(all_vertex, config):

    m = config['constraints']['problem_density'] * len(all_vertex)

    vertex_idx = np.random.choice(len(all_vertex), int(m), replace=False)

    return [all_vertex[i] for i in vertex_idx]


def generate_constraints():

    # Load configuration file
    config = yaml.full_load(open('config.yaml'))

    # Generate all the possible vertex
    all_vertex = list(combinations(range(30), 2))

    # Choose vertex according to the density of the problem
    vertex = choose_vertex(all_vertex, config)

    # Generate ndarray constraint matrix for each vertex
    constraints = generate_constraints_dict(vertex, config)

    # Export the generated constrints
    export_constraints(constraints, config)


# generate_constraints()
