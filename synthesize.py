"""
Tung M. Phan
This module compute realizability relation between assumptions and guarantees
California Institute of Technology
April 16, 2019

"""
import os
import subprocess
import numpy as np
import datetime
from contracts.mutate import Ai, Gi, assumptions, guarantees
current_path = os.path.dirname(os.path.abspath(__file__))

def synthesize_contract(A,G):
    # load template
    inputfile = open(current_path + '/contracts/AG_template.structuredslugs')
    # write to new contract
    outputfile = open(current_path + '/contracts/AG_contract.structuredslugs', 'w')
    outputfile.writelines(inputfile)
    if 'bridge_working' not in set(A): # negative properties
        outputfile.writelines(assumptions['bridge_broken'])
    for a in A:
        if a == "bridge_working":
            pass
        else:
            outputfile.writelines(assumptions[a])
    for g in G:
        outputfile.writelines(guarantees[g])

    inputfile.close()
    outputfile.close()

def check_real(A, G):
    synthesize_contract(A,G)
    cmd = subprocess.run([current_path + '/run', 'check'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    comp_time =cmd.stdout.decode('utf-8')
    val = [int(s) for s in comp_time.split() if s.isdigit()][0]
    real = cmd.stderr.decode('utf-8')
    if ' realizable' in real:
        return True, val
    elif 'unrealizable' in real:
        return False, val


R = dict()
R['comp_time'] = np.zeros([len(Ai),len(Gi)])
R['real_rel'] = np.zeros([len(Ai),len(Gi)], dtype=bool)
R['paired'] = np.zeros([len(Ai),len(Gi)], dtype=bool)
count = 0
total = len(Ai) * len(Gi)
for i in range(1):
    for j in range(1):
        real, comp = check_real(Ai[i],Gi[j])
        R['real_rel'][i][j] = real
        R['comp_time'][i][j] = comp
        R['paired'][i][j] = True
        count += 1
        print('Progress: ' + str(round(count/float(total)*100,3)) + '%')


now = str(datetime.datetime.now())
np.save('R_' + now + '.npy', R)
