# Tung Phan
# April 14, 2019
# This module does calculations involving Galois connections
# California Insitute of Technology 
import numpy as np

def get_fixpoints(oX,oY,R):
    """
    This function computes the fixpoints for the antitone Galois connection
    formed between two sets (represented as tuples) oX, oY induced by the
    binary relation R using Kuznetsov's CbO algorithm
    Input:
    oX - an array of objects/features
    oY - an array of objects/features
    R - a Bool array representing a subset of oX x oY
    Output:
    fixpoints - the set of all fixpoints
    """
    fixpoints = []
    oX = np.array(oX)
    oY = np.array(oY)
    m = len(oX)
    n = len(oY)
    X = set(range(m)) # set of indices for oX
    Y = set(range(n)) # set of indices for oY
    def down(subY):
        """
        Polarity from oY^2 to oX^2
        """
        return {x for x in X if all(R[x,list(subY)])}

    def up(subX):
        """
        Polarity from oX^2 to oY^2
        """
        return {y for y in Y if all(R[list(subX),y])}

    def generate_from(A,B,y):
        """
        The CbO algorithm
        """
        fixpoints.append([oX[list(A)], oY[list(B)]])
        if not(B == Y or y > n):
            for j in range(y,n):
                if j not in B:
                    C = A.intersection(down({j}))
                    D = up(C)
                    Yj = {y for y in Y if y < j}
                    if B.intersection(Yj) == D.intersection(Yj):
                        generate_from(C,D,j + 1)

    generate_from(down(set()), up(down(set())), 0)
    return fixpoints

# test case
#X = np.array(['A0','A1','A2','A3'])
#Y = np.array(['G0','G1','G2','G3','G4','G5'])
#R = np.array([
#     [True, True, True, False, False, False],
#     [True, False, True, True, True, True],
#     [True, True, False, False, True, False],
#     [False, True, True, False, False, False]
#     ])
#
#fixpoints = get_fixpoints(X,Y,R)
#for pair in fixpoints:
#    pair0, pair1 = pair
#    print([set(pair0),set(pair1)])
