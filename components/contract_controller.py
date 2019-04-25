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

A_red, G_red, R_full = make_contracts()
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

def find_assumption_indices(assm, modifier = None):
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

def find_assume_fixpoint(assm):
    """
    given a set of assumptions, return the index of the corresponding fixpoint
    containing it
    """
    global A_red
    assm_idx = find_assumption_indices(assm)
    for i in range(len(A_red)):
        if set(assm_idx) <= set(A_red[i]):
            return i

def principal_filter(base, full_rel = R_full, include_base = True):
    """
    compute the principle filter of an element in a poset defined by full_rel
    """
    filter_ = set()
    for j in range(full_rel.shape[1]):
        if full_rel[j][base]:
            filter_.add(j)
    if include_base:
        filter_.add(base)
    return filter_

def principal_ideal(base, full_rel = R_full, include_base = True):
    """
    compute the principal ideal of an element in a poset defined by full_rel
    """
    ideal_ = set()
    for j in range(full_rel.shape[1]):
        if full_rel[base][j]:
            ideal_.add(j)
    if include_base:
        ideal_.add(base)
    return ideal_

def greedy_controller(A):
    i = find_assume_fixpoint(A)
    all_guarts = set()
    PI = principal_ideal(i, R_full)
    for j in PI:
        all_guarts.union(Ai[j])
    return all_guarts

A = {'r1_near', 'r2_far', 'bridge', 'button1'}

print(greedy_controller(A))
