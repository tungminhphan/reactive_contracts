"""
Contract controller
Tung M. Phan
California Institute of Technology
April 24, 2019
"""
import os, sys
sys.path.append('..') # for import
from contracts.compute_contract_fixpoints import *
from scenarios.abstraction import instructions, DELTA

A_red, G_red = make_contracts()

def to_assumption(concrete_state, failures):
    """
    This function maps a discrete state to an appropriate assumption defined in
    the "instructions" function.

    """
    global DELTA
    assm = set(instructions((concrete_state['x1'],
        concrete_state['y1']),(concrete_state['x2'], concrete_state['y2'])) +
        DELTA)
    return set(assm) - set(failures)

def analyze_assumption(assm):
    """
    Given an assumption, this function returns the current "conditions" of the
    environment.

    """
    has_ = set()
    for artifact in DELTA:
        if artifact in assm:
            has_.add(artifact)
    return has_

def find_guarantees(guart):
    """
    Given guarantee set, this function returns the indices of guarantees that
    are included in the set "guart"
    TODO: optimize this.

    """
    guart = set(guart) # convert to set
    idx = []
    for i in range(len(Gi)):
        if set(Gi[i]) <= guart:
            idx.append(i)
    return idx

def find_assumptions(assm, modifier = None):
    """
    Given assumption, this function returns the indices of assumptions that are
    weaker or stronger than it if modifer is set to "weak" or "strong",
    otherwise it will just return the assumption's index.
    TODO: optimize this.

    """
    global Ai
    idx = []
    assm = set(assm) # conver to set
    for i in range(len(Ai)):
        if modifier == 'weaker':
            if set(Ai[i]) <= assm:
                idx.append(i)
        elif modifier == 'stronger':
            if assm <= set(Ai[i]):
                idx.append(i)
        else:
            if assm == set(Ai[i]):
                idx.append(i)
                return idx
    return idx

