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
from graphviz import Digraph
from sympy import Symbol, simplify_logic

data_num = 4
real_rel = np.load(parent_path + '/data/real_rel' + str(data_num) + '.npy').item()['real_rel']
refi_rel = np.load(parent_path + '/data/refi_rel' + str(data_num) + '.npy')

contract_fixpoints = get_fixpoints(range(len(Ai)), range(len(Gi)), real_rel)

def process_fixpoints(FP):
    """
    Process Galois fixpoints
    input: FP - list of fixpoints
    output: two lists of fixpoints one for each domain

    """
    A = []
    G = []
    for pair in contract_fixpoints:
        assm, guaran = pair
        A.append(assm)
        G.append(guaran)
    return A, G

def get_assume_poset(A):
    """
    input : A - a list of assumptions
    output: R - an ordering relation
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
    input : G - a list of guarantees
    output: R - an ordering relation
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
    input: R - a transitive reduced relation
    output: printed instructions for Hasse diagram
    """
    edge = 0
    n = R.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and R[i][j]:
                edge += 1
                print('edge ' + str(edge) + ': ' + str(i) + ' is contained in ' + str(j))

def create_min_edge_list(R, A = None):
    """
    input: R - a transitive reduced relation
    output: a list of edges induced by R
    """
    edges = []
    n = R.shape[0]
    for i in range(n):
        for j in range(n):
            if i != j and R[i][j]:
                if A != None:
                    if len(A[i]) == 0:
                        Ai = 'Ø'
                    else:
                        Ai = str(A[i])
#                        Ai = str(sorted(A[i])) # sorting for list
                    if len(A[j]) == 0:
                        Aj = 'Ø'
                    else:
                        Aj = str(A[j])
#                        Aj = str(sorted(A[j])) # sorting for list
                    edges.append([Ai,Aj])
                else:
                    edges.append([str(i),str(j)])
    return edges

def convert_to_digraph(edge_list, name):
    poset = Digraph(format='svg')
#    poset.attr('node', shape='circle')
    # adds transitions
    for trans in edge_list:
        state1, state2 = trans
        poset.edge(name+state1, name+state2)
    return poset

def reduce_assume_fixpoints(A):
    """
    input : A - a list of fixpoint assumptions
    output: A_red - a reduced list of fixpoint assumptions
    """
    A_red = []
    RA = transitive_reduce(get_assume_poset(A))
    for i in range(len(A)):
        overlap = set()
        for j in range(len(A)):
            if j != i and RA[j][i]:
                overlap = overlap.union(set(A[j]))
        A_red.append(list(set(A[i]) - overlap))
    return A_red


def simp_assume_disjunct(Aset,Avars):
    ldict = {} # local dictionary has to be created because of a bug in exec()
    A_all = []
    for idx in Aset:
        A_all.append(Ai[idx])
#    Avars = set()
#    for A in A_all:
#        Avars = Avars.union(set(A))
    Avars = Avars
    for var in Avars:
        exec(var + '= Symbol(\'' + var +'\')', globals(), ldict)
    B = None
    for conj in A_all:
        A = None
        for disj in conj:
            if A == None:
                exec('A = ' + disj, locals(), ldict)
                A = ldict['A']
            else:
                exec('A = A & ' + disj, locals(), ldict)
                A = ldict['A']
        if B == None:
            exec('B = A', locals(), ldict)
            B = ldict['B']
        else:
            exec('B = B | A', locals(), ldict)
            B = ldict['B']
    if B != None:
        B = simplify_logic(B, force=True)
        # simplify init conditions
        # TODO: define init to automate this process
        exp1 = ldict['r1_far'] | ldict['r1_near'] | ldict['r1_home']
        exp2 = ldict['r2_far'] | ldict['r2_near'] | ldict['r2_home']
        B = B.subs(exp1, True)
        B = B.subs(exp2, True)
        B = simplify_logic(B, force=True)
    return str(B)

# test case
A, G = process_fixpoints(contract_fixpoints)
A_red = reduce_assume_fixpoints(A)
RA = transitive_reduce(get_assume_poset(A))

Avars = set()
for A in Ai:
    Avars = Avars.union(set(A))

A_red_specs = []
for AI in A_red:
    temp = simp_assume_disjunct(AI,Avars)
    A_red_specs.append(temp)
edge_list = create_min_edge_list(RA, A_red_specs)
#edge_list = create_min_edge_list(RA)

convert_to_digraph(edge_list,'').render(filename='galois', cleanup=True, view=True)
