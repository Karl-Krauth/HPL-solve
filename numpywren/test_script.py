from numpywren.matrix import BigMatrix
from numpywren.matrix import BigSymmetricMatrix
import sys
import scipy.linalg as la
import numpy as np

np.set_printoptions(precision=3)
with open("shape", "r") as f:
    N = int(f.readline().strip())
    NB = int(f.readline().strip())
input = BigSymmetricMatrix(sys.argv[1], shape=[N, N], shard_sizes=[NB, NB]).numpy(36)
input2 = BigMatrix(sys.argv[2], shape=[N, 1000], shard_sizes=[NB, 1000]).numpy(36)
input = np.append(input, input2, axis=1)
output = BigMatrix(sys.argv[1] + ".out", shape=[N, N+1000], shard_sizes=[NB, NB], write_header=True).numpy(36)
P, L, U = la.lu(input)
U2 = np.triu(output)
L2 = np.tril(output)[:, :N] - np.diag(np.diag(output[:, :N])) + np.eye(output.shape[0])
print(input)
print("UPPER REAL")
print(U)
print("UPPER CLUSTER")
print(U2)
print("UPPER DIFF")
print(((U - U2) ** 2).sum())
print("LOWER REAL")
print(L)
print("LOWER CLUSTER")
print(L2)
print("LOWER DIFF")
print(((L - L2) ** 2).sum())

y = U[:, N:]
U = U[:, :N]
x = np.linalg.solve(U, y)
y2 = output[:, N:]
U2 = np.triu(output[:, :N])
x2 = np.linalg.solve(U2, y2)
print("REAL Y")
print(y)
print("CLUSTER Y")
print(y2)
print("Y DIFF")
print(((y - y2)**2).sum())
print("True X ")
print(x)
print("X Solved cluster LU")
print(x2)
print("X DIFF")
print(((x - x2)**2).sum())
