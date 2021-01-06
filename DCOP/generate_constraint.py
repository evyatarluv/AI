"""

This script responsible for generating random constraint for DCOP.

"""
import yaml
from itertools import combinations
import numpy as np
import pickle


def generate_constraints_dict(vertex, config):

    """
    The function get list of tuples and for each tuple generate constraint matrix costs.
    :param config: configuration dict
    :param vertex: list of tuples
    :return: dict where each key is a tuple and the value is ndarray.
    """

    n_domain = len(config['environment']['domain'])
    cost_range = config['constraints']['cost_range']
    toughness = config['constraints']['problem_toughness']
    constraints = {}

    # Compute amount of zeros and non-zeros
    zeros = int((1 - toughness) * (n_domain ** 2))
    non_zeros = (n_domain ** 2) - zeros

    # Create constraints for each vertex
    for v in vertex:

        # Create the constraint according the toughness
        constraint = ([0] * zeros) + list(np.random.randint(cost_range[0], cost_range[1], non_zeros))
        np.random.shuffle(constraint)

        # Append the constraint
        constraints[v] = np.reshape(constraint, (n_domain, n_domain))

    return constraints


def export_constraints(constraints, config):
    """
    Export the constraints as dict for each agent.
    The exported file saves as pickle file.
    :param config: configuration dict
    :param constraints: dict with all the constraints where the key is the vertex and the constraints as ndarray
    :return: dict where the other agent is the key and the constraints as ndarray
    """
    constraints_filename = config['constraints']['filename']['constraints']
    n_agent = config['environment']['n_agents']
    agents_constraints = {a: {} for a in range(n_agent)}  # example: {agent: {other_agent: costs, ...}, ...}

    # Re-construct the dict by agents instead of tuples
    for variables, cost in constraints.items():

        agents_constraints[variables[0]][variables[1]] = cost
        agents_constraints[variables[1]][variables[0]] = cost.T

    # For each agent export the constraints dict
    for agent, costs in agents_constraints.items():

        pickle.dump(costs, open(constraints_filename.format(agent), 'wb'))


def choose_vertex(all_vertices, config):
    """
    This function get a list with all the optional vertex as list of tuples
    and choose the vertex which be in use.
    Additionally the function export the vertices which chosen.
    :param all_vertices: list of tuples with all the optional vertex in the graph
    :param config: configuration dict
    :return: list of tuples with the chosen vertex
    """
    # Get the problem density and compute number of vertices
    m = config['constraints']['problem_density'] * len(all_vertices)

    # Randomize vertices
    vertex_idx = np.random.choice(len(all_vertices), int(m), replace=False)
    vertices = [all_vertices[i] for i in vertex_idx]

    # Export vertices as pickle file
    filename = config['constraints']['filename']['vertices']
    pickle.dump(vertices, open(filename, 'wb'))

    return vertices


def generate_constraints():
    """
    The main function of the script.
    Using the configuration yaml file and generate dict of constraints for each agent.
    The exported file saves as pickle file.
    :return:
    """
    # Load configuration file
    config = yaml.full_load(open('config.yaml'))

    # Set seed
    np.random.seed(config['constraints']['seed'])

    # Generate all the possible vertex
    all_vertices = list(combinations(range(30), 2))

    # Choose vertex according to the density of the problem
    vertices = choose_vertex(all_vertices, config)

    # Generate ndarray constraint matrix for each vertex
    constraints = generate_constraints_dict(vertices, config)

    # Export the generated constraints
    export_constraints(constraints, config)


generate_constraints()
