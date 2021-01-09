"""

This script responsible for generating random constraint for DCOP.

The script create n constraint for each agent. Each constraint is a dict where the key is the neighbor
id and the value is the cost matrix, i.e., constraints look as follows:
{ neighbor_id (int): costs (ndarray), ..... }

The script create n constraints according to the agents' amount.

Other configurations like constraints' filename, n_domain, n_agents can be found in the `config.yaml` file.

"""
import os
from itertools import combinations
import numpy as np
import pickle
from typing import List, Tuple, Dict, Any
from pathlib import Path

# Root project directory
root_project = Path(__file__).parent.parent


def generate_constraints_dict(edges: List[Tuple[int, int]],
                              config: Dict[str, Any]) -> Dict[Tuple[int, int], np.array]:

    """
    The function get list of tuples and for each tuple generate constraint matrix costs.
    :param config: configuration dict
    :param edges: list of tuples
    :return: dict where each key is a tuple and the value is ndarray.
    """

    n_domain = config['environment']['n_domain']
    cost_range = config['constraints']['cost_range']
    toughness = config['constraints']['problem_toughness']
    constraints = {}

    # Compute amount of zeros and non-zeros
    zeros = int((1 - toughness) * (n_domain ** 2))
    non_zeros = (n_domain ** 2) - zeros

    # Create constraints for each edge
    for e in edges:

        # Create the constraint according the toughness
        constraint = ([0] * zeros) + list(np.random.randint(cost_range[0], cost_range[1], non_zeros))
        np.random.shuffle(constraint)

        # Append the constraint
        constraints[e] = np.reshape(constraint, (n_domain, n_domain))

    return constraints


def export_constraints(constraints: Dict[Tuple[int, int], np.array],
                       config: Dict[str, Any]):
    """
    Export the constraints as dict for each agent.
    The exported file saves as pickle file.
    :param config: configuration dict
    :param constraints: dict with all the constraints where the key is the edge and the constraints as ndarray
    :return: dict where the other agent is the key and the constraints as ndarray
    """
    constraints_filename = os.path.join(root_project, config['constraints']['filename']['constraints'])
    n_agent = config['environment']['n_agents']
    agents_constraints = {a: {} for a in range(n_agent)}  # example: {agent: {other_agent: costs, ...}, ...}

    # Re-construct the dict by agents instead of tuples
    for variables, cost in constraints.items():

        agents_constraints[variables[0]][variables[1]] = cost
        agents_constraints[variables[1]][variables[0]] = cost.T

    # For each agent export the constraints dict
    for agent, costs in agents_constraints.items():

        pickle.dump(costs, open(constraints_filename.format(agent), 'wb'))


def choose_edges(config: Dict[str, Any]) -> List[Tuple[int, int]]:
    """
    This function get a list with all the optional edges as list of tuples
    and choose the edges which be in use.
    Additionally the function export the edges which chosen.
    :param config: configuration dict
    :return: list of tuples with the chosen edges
    """

    # Create all edges
    all_edges = list(combinations(range(config['environment']['n_agents']), 2))
    m = config['constraints']['problem_density'] * len(all_edges)

    # Choose edges according given problem density
    edges_idx = np.random.choice(len(all_edges), int(m), replace=False)
    edges = [all_edges[i] for i in edges_idx]

    # Export vertices as pickle file
    filename = os.path.join(root_project, config['constraints']['filename']['edges'])
    pickle.dump(edges, open(filename, 'wb'))

    return edges


def generate_constraints(config: Dict[str, Any]):
    """
    The main function of the script.
    Using the configuration yaml file to generate dict of constraints for each agent.
    The exported file saves as pickle file.
    :return:
    """

    # Set seed
    np.random.seed(config['constraints']['seed'])

    # Choose edges according to the density of the problem
    edges = choose_edges(config)

    # Generate ndarray constraint matrix for each vertex
    constraints = generate_constraints_dict(edges, config)

    # Export the generated constraints
    export_constraints(constraints, config)
