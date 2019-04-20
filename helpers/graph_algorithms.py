"""
Tung Phan
April 19, 2019
California Institute of Technology
Simple algorithm to transitive reduce an (acyclic) graph
"""
import numpy as np

def transitive_reduce(A):
    """
    input: A is a reachability Boolean numpy array
    output: transitive reduced version of A
    """
    n = A.shape[0]
    for i in range(n):
        for j in range(n):
            if A[i][j] and i != j:
                for k in range(n):
                    if k != i and k !=j and A[i][k] and A[k][j]:
                        A[i][j] = False
    return A

#test case
#A = np.array([[1,0,0,0],[1,1,0,0],[1,0,1,0],[1,0,1,1]])
#print(transitive_reduce(A))



