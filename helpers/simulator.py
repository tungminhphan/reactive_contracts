"""
Tung Phan
February 18, 2019
This module reads a strategy .npy file and creates a random trace
(of specified length)
"""

import sys
import numpy as np


def load_strategy():

    if __name__ == '__main__':
        filename = '../contracts/AG_contract'
    else:
        filename = str(sys.argv[1])

    strategy_dict = np.load(filename+'.npy', allow_pickle=True).item()
    return strategy_dict

# variables_to_collect = ['x1', 'y1', etc.] is an ordered tuple
def run_from(max_steps, variables_to_collect, init_state = 'random'):
    """
    create a simulation trace
    """
    run = [] # trace to broadcast
    def look_up_state_id(state):
        """
        look for a dictionary that contains the subdictionary "state"
        """
        for key in strategy_dict:
            if state.items() <= strategy_dict[key].items():
                return key
    def collect():
        """
        append the current state's values of interest to run

        """
        collect_state = [] # values to save for variables specified in variables_to_collect
        for var in variables_to_collect:
            collect_state.append(strategy_dict[current_state][var])
        run.append(collect_state)

    # load initial strategy
    strategy_dict = load_strategy()
    # compute initial state
    steps = 0
    if init_state == 'random':

        current_state = np.random.choice(tuple(strategy_dict))
    else:
        current_state = look_up_state_id(init_state)
    collect()

    # next step
    while steps < max_steps:
        if '' not in strategy_dict[current_state]['successors']:
            steps += 1
            next_states = strategy_dict[current_state]['successors']
            current_state = np.random.choice(tuple(next_states))
            collect()
        else:
            break
    return run
