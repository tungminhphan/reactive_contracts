# Tung Phan
# April 11, 2019
# This module generates jumps in assertions

import os
current_path = os.path.dirname(os.path.abspath(__file__))

# write to new contract
outputfile = open(current_path + '/AG_contract.structuredslugs', 'w')

assumptions = dict()
guarantees = dict()

assumptions['ego1_start'] = r"""
[ENV_INIT]
x1<=2
y1<=1
"""
assumptions['ego1_near'] = r"""
[ENV_INIT]
x1<=1
y1>=3
"""
assumptions['ego1_far'] = r"""
[ENV_INIT]
x1>=3
y1>=3
"""
assumptions['ego2_start'] = r"""
[ENV_INIT]
x2<=2
y2<=1
"""
assumptions['ego2_near'] = r"""
[ENV_INIT]
x2<=1
y2>=3
"""
assumptions['ego2_far'] = r"""
[ENV_INIT]
x2>=3
y2>=3
"""
assumptions['button1_working']  = r"""
[ENV_TRANS]
# button1 behavior
((x1 = 0 & y1 = 1) | (x2 = 0 & y2 = 1)) -> bridge'
"""
assumptions['button2_working']  = r"""
[ENV_TRANS]
# button2 behavior
((x1=0 & y1=3) | (x2=0 & y2=3)) -> bridge'
"""
assumptions['bridge_broken'] = r"""
[SYS_TRANS]
# far bridge is
!(x1=2 & y1=4)
!(x2=2 & y2=4)
"""

guarantees['box_far'] = r"""
[SYS_LIVENESS]
box=3
"""
guarantees['box_near'] = r"""
[SYS_LIVENESS]
box=2
"""
guarantees['ego2_far'] = r"""
[SYS_LIVENESS]
x2 = 4 & y2 =3
"""
guarantees['ego2_near'] = r"""
[SYS_LIVENESS]
x2=0 & y2=4
"""
guarantees['ego2_start'] = r"""
[SYS_LIVENESS]
x2=2 & y2=0
"""
guarantees['box_ego2_near'] = r"""
[SYS_LIVENESS]
x2=0 & y2=4 & box=2
"""
guarantees['box_ego2_far'] = r"""
[SYS_LIVENESS]
x2 = 4 & y2 =3 & box=3
"""

def get_assumptions():
    loc = {'start', 'near', 'far'}
    safe = {'button1', 'button2', 'bridge'}
    assumptions = []
    for ego1 in loc:
        ego1 = 'ego1_' + ego1
        for ego2 in loc:
            ego2 = 'ego2_' + ego2
            for button1_working in {True, False}:
                for button2_working in {True, False}:
                    for bridge_working in {True, False}:
                        assumption = [ego1, ego2]
                        if button1_working:
                            assumption.append('button1_working')
                        if button2_working:
                            assumption.append('button2_working')
                        if bridge_working:
                            assumption.append('bridge_working')
                        assumptions.append(assumption)
    return assumptions

def get_guarantees():
    loc_box = {'near', 'far', None}
    loc2 = {'start', 'near', 'far', None}
    guarantees = []
    for ego2 in loc2:
        if ego2 != None:
           ego2 = 'ego2_' + ego2
        for box in loc_box:
            if box != None:
                box = 'box_' + box
            for box_ego2 in loc_box:
                if box_ego2 != None:
                    choice = box_ego2
                    box_ego2 = 'box_ego2_' + box_ego2
                    if box == 'box_' + choice:
                        box = None
                    if ego2 == 'ego2_' + choice:
                        ego2 = None
                guarantee = []
                if box_ego2 != None:
                    guarantee.append(box_ego2)
                if ego2 != None:
                    guarantee.append(ego2)
                if box != None:
                    guarantee.append(box)
                if guarantee != []:
                    guarantees.append(guarantee)
    return guarantees

Ai = get_assumptions()
Gi = get_guarantees()


def synthesize_contract(A,G):
    # load template
    inputfile = open(current_path + '/AG_template.structuredslugs')
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

A = Ai[50]
G = Gi[3]
print(A)
print(G)
synthesize_contract(A,G)

inputfile.close()
outputfile.close()
