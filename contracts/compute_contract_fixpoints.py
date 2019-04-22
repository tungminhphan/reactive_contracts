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
from contracts.generate_AG import Ai, Gi, assumptions, guarantees
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
    n = len(G)
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

def create_min_edge_list(R, A = None, empty = set(), AG = ''):
    """
    input: R - a transitive reduced relation
    input: A - an index list of assumes/guarantees
    input: empty - list that should be "empty"
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
                        if i in empty:
                            Ai = '∧ (' + str(i) + ')'
                        else:
                            Ai = str(A[i])
#                        Ai = str(sorted(A[i])) # sorting for list
                    if len(A[j]) == 0:
                        Aj = 'Ø'
                    else:
                        if j in empty:
                            Aj = '∧ (' + str(j) + ')'
                        else:
                            Aj = str(A[j])
#                        Aj = str(sorted(A[j])) # sorting for list
                    edges.append([Ai,Aj])
                else:
                    edges.append([str(i),str(j)])
    return edges

def convert_to_digraph(node_list, edge_list, name):
    poset = Digraph(format='svg')
#    poset.attr('node', color='skyblue', style='filled')
    # adds transitions
    for trans in edge_list:
        state1, state2 = trans
        if state1[0] != '∧' and state1 != 'None':
            state1 = name + state1
        if state2[0] != '∧' and state2 != 'None':
            state2 = name + state2
        poset.edge(state1, state2)
#    for i in range(len(node_list)):
#        print(node_list)
#        node = str(Gi[i])
#        poset.node(node, color="/spectral9/"+str(i+1))
    return poset

def reduce_fixpoints(B, AG = None): # B is either 'assume' or 'guarantee'
    """
    input : A - a list of fixpoint assumptions
    output: A_red - a reduced list of fixpoint assumptions
    output: RA - a reduced relation
    """

    B_red = []
    empty = set()
    if AG == 'assume':
        RB = transitive_reduce(get_assume_poset(B))
        RBc = RB
    elif AG == 'guarantee':
        RB = transitive_reduce(get_guarantee_poset(B))
        RBc = np.array(RB).transpose()
    for i in range(len(B)):
        overlap = set()
        for j in range(len(B)):
            if j != i and RBc[j][i]:
                overlap = overlap.union(set(B[j]))

        if len(B[i]) > 0 and len(set(B[i])-overlap) == 0 and AG == 'guarantee':
            B_red.append(list(set(B[i])))
            empty.add(i)
        else:
            B_red.append(list(set(B[i]) - overlap))
    return B_red, RB, empty


def simp_assume_disjunct(Aset, Avars):
    """
    Convert a disjunction oof assumptions to an equivalent an Boolean expression
    input: Aset - a list of assumptions disjuncts
           Avars - set of all variables involved in the disjuncts
    output: an equivalent Boolean expression
    """
    ldict = {} # local dictionary has to be created because of a bug in exec()
    A_all = [] #
    for idx in Aset:
        A_all.append(Ai[idx])
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

def simp_guarantee_conjunct(Gset, Gvars):
    """
    Convert a conjunction of guarantees to an equivalent an Boolean expression
    input: Gset - a list of guarantee conjuncts
           Gvars - set of all variables involved in the conjuncts
    output: an equivalent Boolean expression
    """
    ldict = {}
    G_all = []
    for idx in Gset: # picks out guarantees from a particular fixpoint
        G_all.append(Gi[idx])
    for var in Gvars:
        exec(var + '= Symbol(\'' + var +'\')', globals(), ldict)
    B = None
    for disj in G_all:
        A = None
        for conj in disj:
            if A == None:
                exec('A = ' + conj, locals(), ldict)
                A = ldict['A']
            else:
                exec('A = A | ' + conj, locals(), ldict) # TODO: check
                A = ldict['A']
        if B == None:
            exec('B = A', locals(), ldict)
            B = ldict['B']
        else:
            exec('B = B & A', locals(), ldict)
            B = ldict['B']
    if B != None:
        B = simplify_logic(B, force=True)
    return str(B)

def make_contracts():
    A, G = process_fixpoints(contract_fixpoints)

    # guarantees
    G_red, RG, empty = reduce_fixpoints(G,'guarantee')
    Gvars = set()
    for g in Gi:
        Gvars = Gvars.union(set(g))

    G_red_specs = []
    for GI in G_red:
        temp = simp_guarantee_conjunct(GI,Gvars)
        G_red_specs.append(temp)

    guarantee_edge_list = create_min_edge_list(RG, G_red_specs, empty)
    convert_to_digraph(G_red, guarantee_edge_list,'□◇').render(filename='galois_guarantee', cleanup=True, view=True)

    # assumptions
    A_red, RA, empty = reduce_fixpoints(A,'assume')
    Avars = set()
    for a in Ai:
        Avars = Avars.union(set(a))

    A_red_specs = []
    for AI in A_red:
        temp = simp_assume_disjunct(AI,Avars)
        A_red_specs.append(temp)

    assume_edge_list = create_min_edge_list(RA, A_red_specs, empty)
    convert_to_digraph(assume_edge_list,'').render(filename='galois_assume', cleanup=True, view=True)
    edge_list = assume_edge_list + guarantee_edge_list

make_contracts()
