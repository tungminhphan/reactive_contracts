"""
Tung M. Phan
This module computes contract fixpoints induced by the realizability relation
between the assumption and guarantee sets
California Institute of Technology
April 16, 2019

"""
import os, sys
import numpy as np
from compute_refinement import assume_refine, guarantee_refine
sys.path.append('..') # for import
from helpers.galois_connections import get_fixpoints
from helpers.graph_algorithms import transitive_reduce
from contracts.mutate import Ai, Gi, assumptions, guarantees
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) # for abs path

data_num = 4
real_rel = np.load(parent_path + '/data/real_rel' + str(data_num) + '.npy').item()['real_rel']
refi_rel = np.load(parent_path + '/data/refi_rel' + str(data_num) + '.npy')

contract_fixpoints = get_fixpoints(range(len(Ai)), range(len(Gi)), real_rel)
A = []
G = []
for pair in contract_fixpoints:
    assm, guaran = pair
    A.append(assm)
    G.append(guaran)

def get_assume_poset(A):
    """
    input - A: list of assumptions
    output -R: an ordering relation
    """
    n = len(A)
    R = np.zeros((n,n),dtype=bool)
    for i in range(n):
        a = set(A[i])
        for j in range(n):
            b = set(A[j])
            if assume_refine(a,b) and a != b:
                R[i][j] = True
    return R

def get_guarantee_poset(G):
    """
    input - A: list of assumptions
    output -R: an ordering relation
    """
    n = len(A)
    R = np.zeros((n,n),dtype=bool)
    for i in range(n):
        a = set(G[i])
        for j in range(n):
            b = set(G[j])
            if guarantee_refine(a,b) and a != b:
                R[i][j] = True
    return R

def print_instructions(R):
    """
    input - R: a transitive reduced relation
    output: instructions for Hasse diagram
    """
    edge = 0
    n = R.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and R[i][j]:
                edge += 1
                print('edge ' + str(edge) + ': ' + str(i) + ' is contained in ' + str(j))


# test case

# print_instructions(transitive_reduce(get_guarantee_poset(G)))

#print([Ai[i] for i in A[4]])
#print('\n')
#print([Gi[i] for i in G[2]])
#contract_fixpoints = get_fixpoints(Ai, Gi, real_rel)
#
#A = []
#G = []
#
#for pair in contract_fixpoints:
#    assm, guaran = pair
#    A.append(assm)
#    G.append(guaran)
#
