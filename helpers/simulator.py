# Tung Phan
# February 18, 2019
# This module reads a strategy .npy file and creates a random trace
# (of specified length)

import sys
import numpy as np
filename = str(sys.argv[1])
strategy_dict = np.load(filename+'.npy').item()

# variables_to_collect = ['x1', 'y1', etc.] is an ordered tuple
def random_run_from(init_state, max_steps, variables_to_collect):
    current_state = init_state
    steps = 0

    collect_state = []
    for var in variables_to_collect:
        collect_state.append(strategy_dict[current_state][var])

    run = [collect_state]
    while '' not in strategy_dict[current_state]['successors'] and steps < max_steps:
        next_states = strategy_dict[current_state]['successors']
        current_state = np.random.choice(tuple(next_states))
        collect_state = []
        for var in variables_to_collect:
            collect_state.append(strategy_dict[current_state][var])
        run.append(collect_state)
        steps += 1
    return run
