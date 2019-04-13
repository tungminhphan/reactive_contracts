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
x1<=2
y1<=1
x2<=2
y2<=1
!bridge
box=0
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
outputfile.writelines(inputfile)

# ASSUMPTIONS
outputfile.writelines(assumptions['init'])
outputfile.writelines(assumptions['button1'])
outputfile.writelines(assumptions['button2'])

# GUARANTEES
outputfile.writelines(guarantees['box_near'])
outputfile.writelines(guarantees['box_far'])
outputfile.writelines(guarantees['ego2_far'])
outputfile.writelines(guarantees['ego2_near'])

inputfile.close()
outputfile.close()
