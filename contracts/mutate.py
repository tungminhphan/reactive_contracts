# Tung Phan
# April 11, 2019
# This module generates jumps in assertions

import os
import numpy as np
import itertools
current_path = os.path.dirname(os.path.abspath(__file__))

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
def get_powerset(s):
    '''
    Compute the powerset of a set by shifting bits
    '''
    x = len(s)
    Ps = []
    for i in range(1 << x): # 1 << x is 1 shifted to the left x times, this is the same as multiplying 1 by 2**x
        Ps.append([s[j] for j in range(x) if (i & (1 << j))]) # shift and use bitwise "and" to check for "hits" on i
    return Ps

def get_assumptions():
    ego1 = [['ego1_start'], ['ego1_near'], ['ego1_far']]
    ego2 = [['ego2_start'], ['ego2_near'], ['ego2_far']]
    safe = get_powerset(['button1_working', 'button2_working', 'bridge_working'])
    assumptions = []
    for A in itertools.product(ego1,ego2,safe):
        a = []
        for part in A:
            a = a + part
        if a != []:
            assumptions.append(a)
    return assumptions

def get_guarantees():
    """
    singleton version
    """
    guarantees = [['ego2_start'], ['ego2_near'], ['ego2_far'], ['box_near'],['box_far'],['box_ego2_near'],['box_ego2_far']]
    return guarantees

def get_guarantees2():
    """
    powerset version
    """
    guarantees = []
    # absence of joint box_ego2
    ego2 = get_powerset(['ego2_start', 'ego2_near', 'ego2_far'])
    box = get_powerset(['box_near', 'box_far'])
    for G in itertools.product(ego2,box):
        g = []
        for part in G:
            g = g + part
        if g != []:
            guarantees.append(g)
    # presence of joint box_ego2
    for loc in ['near', 'far']:
        oploc = 'near'
        if loc == 'near':
            oploc = 'far'
        box_ego2 = [['box_ego2_' + loc]]
        ego2 = get_powerset(['ego2_start', 'ego2_' + oploc])
        box = get_powerset(['box_'+oploc])
        for G in itertools.product(box_ego2,ego2,box):
            g = []
            for part in G:
                g = g + part
            if g != []:
                guarantees.append(g)
    return guarantees

Ai = get_assumptions()
Gi = get_guarantees()

# TEST
#A = Ai[np.random.randint(len(Ai))]
#G = Gi[np.random.randint(len(Gi))]
#synthesize_contract(A,G)
