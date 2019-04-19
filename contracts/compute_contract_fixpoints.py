"""
Tung M. Phan
This module computes contract fixpoints induced by the realizability relation
between the assumption and guarantee sets
California Institute of Technology
April 16, 2019

"""
import os, sys
import numpy as np
sys.path.append('..') # for import
from helpers.galois_connections import get_fixpoints
from contracts.mutate import Ai, Gi, assumptions, guarantees
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) # for abs path

real_rel = np.load(parent_path + '/data/real_rel.npy').item()['real_rel']
refi_rel = np.load(parent_path + '/data/refi_rel.npy')

contract_fixpoints = get_fixpoints(Ai, Gi, real_rel)

#for pair in contract_fixpoints:
#    pair0, pair1 = pair
#    print(set(pair0),set(pair1))
