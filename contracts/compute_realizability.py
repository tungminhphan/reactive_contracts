"""
Tung M. Phan
This module computes realizability relation between assumptions and guarantees
California Institute of Technology
April 16, 2019

"""
import os, sys
import subprocess
import numpy as np
import datetime
if __name__ == '__main__':
    from generate_AG import Ai, Gi, assumptions, guarantees, conjoin_guarantees
else:
    from contracts.generate_AG import Ai, Gi, assumptions, guarantees, conjoin_guarantees
current_path = os.path.dirname(os.path.abspath(__file__)) # for abs path
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) # for abs path

def synthesize_contract(A,G):
    #TODO: modularize
    """
    This function takes a pair of assumption and guarantee and convert them to
    a form checkable by slugs which is saved as a structuredslugs file
    """
    # load template
    inputfile = open(current_path + '/AG_template.structuredslugs')
    # write to new contract
    outputfile = open(current_path + '/AG_contract.structuredslugs', 'w')
    outputfile.writelines(inputfile)
    if 'bridge' not in set(A): # negative properties
        outputfile.writelines(assumptions['bridge_broken'])
    for a in A:
        if a == "bridge":
            pass
        else:
            outputfile.writelines(assumptions[a])
    for g in G:
        outputfile.writelines(guarantees[g])

    inputfile.close()
    outputfile.close()

def check_real(A, G):
    """
    This function calls slugs to check if (A,G) is realizable
    """
    synthesize_contract(A,G)
    cmd = subprocess.run([parent_path + '/run', 'syn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    comp_time =cmd.stdout.decode('utf-8')
    val = [int(s) for s in comp_time.split() if s.isdigit()][0]
    real = cmd.stderr.decode('utf-8')
    if ' realizable' in real:
        return True, val
    elif 'unrealizable' in real:
        return False, val

def synthesize_by_Lij(Li, Lj):
    """
    This function creates (Ai[i],Gi[j]). Li and Lj are lists of indices.
    """
    synthesize_contract(Ai[Li[0]], conjoin_guarantees(Lj))

def check_all():
    """
    Run this function to check the realizability of all A/G pairings from Ai x Gi
    """
    R = dict()
    R['comp_time'] = np.zeros([len(Ai),len(Gi)])
    R['real_rel'] = np.zeros([len(Ai),len(Gi)], dtype=bool)
    R['paired'] = np.zeros([len(Ai),len(Gi)], dtype=bool)
    count = 0
    total = len(Ai) * len(Gi)
    now = str(datetime.datetime.now())
    for i in range(len(Ai)):
        for j in range(len(Gi)):
            print('checking A' + str(i) + ' against G' + str(j) + '...')
            real, comp = check_real(Ai[i],Gi[j])
            R['real_rel'][i][j] = real
            R['comp_time'][i][j] = comp
            R['paired'][i][j] = True
            count += 1
            print('Progress: ' + str(round(count/float(total)*100,3)) + '%')
            np.save('contracts/Real_' + now + '.npy', R)
