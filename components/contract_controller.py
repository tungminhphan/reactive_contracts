#!/usr/local/bin/python
# Contract controller
# Tung M. Phan
# California Institute of Technology
# April 24, 2019
import os, sys
sys.path.append('..') # for import
from contracts.compute_contract_fixpoints import *


def state_to_contract(state, instructions):
    """
    This function maps a state to the "best" contract for that state
    """
    return 0

A_red, G_red = make_contracts()
for i in range(len(A_red)):
    print(i)
    for a in A_red[i]:
        print(Ai[a])
    for g in G_red[i]:
        print(Gi[g])

