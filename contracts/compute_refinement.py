"""
Tung M. Phan
This module processes, computes refinement
California Institute of Technology
April 16, 2019

"""
import numpy as np
import datetime
import sys
sys.path.append("..")
from contracts.mutate import Ai, Gi, assumptions, guarantees

def assume_refine(a1, a2):
    return set(a1) <= set(a2)

def guarantee_refine(g1, g2):
    return set(g2) <= set(g1)

def contract_refine(c1, c2):
    a1 = c1['assume']
    a2 = c2['assume']
    g1 = c1['guarantee']
    g2 = c2['guarantee']
    return assume_refine(a1,a2) and guarantee_refine(g1,g2)

def make_contract(a,g):
    return {'assume': a, 'guarantee': g}

Ref = np.zeros((len(Ai),len(Gi),len(Ai),len(Gi)), dtype=bool)

for i in range(len(Ai)):
    for j in range(len(Gi)):
        C_ij = make_contract(Ai[i],Gi[j])
        for k in range(len(Ai)):
            for l in range(len(Gi)):
                C_kl = make_contract(Ai[k],Gi[l])
                Ref[i][j][k][l] = contract_refine(C_ij, C_kl)

now = str(datetime.datetime.now())
if __name__ == '__main__': # if called directly, save output
    np.save('Refi_' + now + '.npy', Ref)
