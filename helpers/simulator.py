"""
Tung Phan
February 18, 2019
This module maniplates and synthesizes from strategy files and creates a random
trace (of specified maximum length)
"""

import sys, os
import numpy as np
import warnings
import subprocess
sys.path.append('..')
from contracts.compute_realizability import synthesize_by_Lij, synthesize_contract
from components import contract_controller
current_path = os.path.dirname(os.path.abspath(__file__)) # for abs path
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) # for abs path

strategy_dict = dict() # initialize strategy

def load_strategy():
    global strategy_dict
    if __name__ == '__main__':
        filename = '../contracts/AG_contract'
    else:
        filename = str(sys.argv[1])
    strategy_dict = np.load(filename+'.npy', allow_pickle=True).item()

# variables_to_collect = ['x1', 'y1', etc.] is an ordered tuple
def run_from(max_steps, variables_to_collect, **options):
    """
    create a simulation trace
    """
    def look_up_state_id(state):
        """
        look for a dictionary that contains the subdictionary "state"
        """
        global strategy_dict
        for key in strategy_dict:
            if state.items() <= strategy_dict[key].items():
                return key
    def collect():
        """
        append the current state's values of interest to "run"

        """
        nonlocal current_state_id
        global strategy_dict
        collect_state = [] # values to save for variables specified in variables_to_collect
        for var in variables_to_collect:
            collect_state.append(strategy_dict[current_state_id][var])
        run.append(collect_state)

    def initialize():
        """
        load initial strategy to simulate (synthesize a new one if necessary),
        collect() newly computed state

        """
        nonlocal current_state_id
        global strategy_dict
        if 'init_contract' not in options: # if init_contract i
            warnings.warn('Using most recently attempted strategy!')
        else:
            init_state, guart = options['init_contract']
            failures = options['init_fail']
            assm = contract_controller.to_assumption(init_state, failures)
            synthesize_contract(assm, guart)
            subprocess.run([parent_path + '/run', 'resyn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # synthesize strategy online
        # load initial strategy
        load_strategy()
        if 'init_state' not in options: # if the initial state is not specified, then it will be randomly chosen
            current_state_id = np.random.choice(tuple(strategy_dict))
        else:
            current_state_id = look_up_state_id(options['init_state'])
        collect()

    def cont(): # continue simulation
        """
        proceed to compute the next step to take according to the current
        strategy

        """
        nonlocal current_state_id, steps
        global strategy_dict
        steps += 1
        next_states = strategy_dict[current_state_id]['successors']
        current_state_id = np.random.choice(tuple(next_states))
        collect()

    def stuck():
        """
        check if a deadend was reached
        """
        nonlocal current_state_id
        global strategy_dict
        return '' in strategy_dict[current_state_id]['successors']

    def fail():
        """
        simulate failure
        """
        if 'fail_prob' not in options:
            fail_prob = 0
        else:
            fail_prob = options['fail_prob']

        return np.random.rand() < fail_prob

    def resynthesize(Li,Lj):
        """
        resynthesize strategy (after failure) for i j being lists of assms and guarts

        """
        nonlocal current_state_id
        global strategy_dict
        synthesize_by_Lij(Li,Lj)
        subprocess.run([parent_path + '/run', 'resyn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # synthesize strategy online
        # load new strategy
        load_strategy()
        current_state_id = np.random.choice(tuple(strategy_dict))
        collect()

    def update_current_state_id(current_state):
        """
        update current state id to corresponding key in new strategy dictionary
        """
        nonlocal current_state_id
        global strategy_dict
        for key in strategy_dict:
            x1 = strategy_dict[key]['x1'] == current_state['x1']
            y1 = strategy_dict[key]['y1'] == current_state['y1']
            x2 = strategy_dict[key]['x2'] == current_state['x2']
            y2 = strategy_dict[key]['y2'] == current_state['y2']
            box = strategy_dict[key]['box'] == current_state['box']
            if x1 and y1 and x2 and y2 and box:
                current_state_id = key
                return None
        print("error: current state doesn't exist in strategy!")

    def react_to(failures, controller = 'greedy'):
        """
        invoke contract controller to react to failures
        """
        nonlocal current_state_id
        global strategy_dict
        init_state, guart = options['init_contract']
        failures = options['init_fail']
        assm = contract_controller.to_assumption(init_state, failures)
        if controller == 'greedy':
            guart = list(contract_controller.greedy_controller(assm))
        synthesize_contract(assm,guart)
        subprocess.run([parent_path + '/run', 'resyn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # synthesize strategy online
        # load new strategy
        current_state = strategy_dict[current_state_id]
        load_strategy()
        update_current_state_id(current_state)
        collect()

    # initialization
    steps = 0
    current_state_id = None
    run = [] # trace to broadcast

    # initialize contract and starting state
    print('synthesizing from initial contract...')
    initialize()
    done = False

    while steps < max_steps:
        print('simulating time step ' + str(steps))
        if steps > 100 and not done:
            failure = np.random.choice(['bridge', 'button1', 'button2'])
            print(failure + ' has failed at time step ' + str(steps) + '!')
            print('attempting to resolve failure...')
            react_to(failure)
            done = True
        elif not stuck():
            cont()
        else:
            break
    return run
