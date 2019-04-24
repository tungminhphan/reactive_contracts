"""
Tung M. Phan
This module generates Hasse diagrams for assume and guarantee lattices
between the assumption and guarantee sets
California Institute of Technology
April 24, 2019

"""
import sys
if __name__ == '__main__':
    sys.path.append('..') # for import
from compute_contract_fixpoints import *
make_contracts(plot=True)

