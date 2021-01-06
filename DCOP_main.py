from DCOP.Mailer import Mailer
from DCOP.DSA import DSA
from DCOP.Agent import Agent
# import DCOP.generate_constraint as constraint
import yaml
import pickle
from typing import List, Dict


def init_agents(mailer: Mailer, config):
    """

    :param mailer:
    :param config:
    :return:
    """

    agents_type = config['environment']['agents_type']
    n_agents = config['environment']['n_agents']
    domain = range(config['environment']['n_domain'])
    constraint_filename = 'DCOP/' + config['constraints']['filename']['constraints']
    agents = []

    # Init agents according to the agent type
    if agents_type.lower() == 'dsa':

        for i in range(n_agents):

            # Init DSA params
            constraints = pickle.load(open(constraint_filename.format(i), 'rb'))
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


def main():

    # Load configuration file
    config = yaml.full_load(open('DCOP/config.yaml'))

    # If we don't have constraints generate them
    # constraint.generate_constraints(config)

    # Init params
    mailer = Mailer()
    agents = init_agents(mailer, config)
    n_iteration = config['environment']['n_iteration']

    # Solve
    for i in range(n_iteration):

        # Move messages to inbox
        mailer.assign_messages()

        # Run each agent iteration
        for a in agents:

            a.iteration(mailer)

        # todo: Compute current iteration cost


if __name__ == '__main__':

    main()