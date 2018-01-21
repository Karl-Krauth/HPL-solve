from numpywren.matrix import BigMatrix
import sys
import scipy.linalg as la
import numpy as np

np.set_printoptions(precision=3)
with open("shape", "r") as f:
    N = int(f.readline().strip())
    NB = int(f.readline().strip())
input = BigMatrix(sys.argv[1], shape=[N, N], shard_sizes=[NB, NB]).numpy()
output = BigMatrix(sys.argv[1] + ".out").numpy()
P, L, U = la.lu(input)
U2 = np.triu(output)
L2 = np.tril(output) - np.diag(np.diag(output)) + np.eye(output.shape[0])

print("UPPER REAL")
print(U)
print("UPPER CLUSTER")
print(U2)

print("LOWER REAL")
print(L)
print("LOWER CLUSTER")
print(L2)
