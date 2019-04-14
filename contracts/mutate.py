# Tung Phan
# April 11, 2019
# This module generates jumps in assertions

import os
current_path = os.path.dirname(os.path.abspath(__file__))

# load template
inputfile = open(current_path + '/AG_template.structuredslugs')
# write to new contract
outputfile = open(current_path + '/AG_contract.structuredslugs', 'w')

assumptions = dict()
guarantees = dict()

assumptions['button1']  = r"""
[ENV_TRANS]
# button1 behavior
((x1 = 0 & y1 = 1) | (x2 = 0 & y2 = 1)) -> bridge'
"""
assumptions['button2']  = r"""
[ENV_TRANS]
# button2 behavior
((x1=0 & y1=3) | (x2=0 & y2=3)) -> bridge'
"""
assumptions['init'] = r"""
[ENV_INIT]
!bridge
box=0
"""
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
guarantees['ego2_recharge'] = r"""
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

outputfile.writelines(inputfile)

# ASSUMPTIONS
outputfile.writelines(assumptions['init'])
outputfile.writelines(assumptions['ego1_near'])
outputfile.writelines(assumptions['ego2_far'])
outputfile.writelines(assumptions['button1'])
outputfile.writelines(assumptions['button2'])
#outputfile.writelines(assumptions['bridge_broken'])

# GUARANTEES
outputfile.writelines(guarantees['box_near'])
#outputfile.writelines(guarantees['box_far'])
outputfile.writelines(guarantees['ego2_recharge'])
#outputfile.writelines(guarantees['ego2_far'])
outputfile.writelines(guarantees['ego2_near'])
outputfile.writelines(guarantees['box_ego2_near'])
#outputfile.writelines(guarantees['box_ego2_far'])

inputfile.close()
outputfile.close()
