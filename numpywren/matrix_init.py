import numpy as np
from numpywren.matrix_init import local_numpy_init
import sys
N = int(sys.argv[1])
NB = int(sys.argv[2])
x = np.random.rand(N, N)
x = x + x.T
print(N, NB)
mat = local_numpy_init(x, [NB, NB], n_jobs=36, symmetric=True, write_header=True)
print("Uploaded A")
mat2 = local_numpy_init(np.random.rand(N, 1000), [NB, 1000], n_jobs=36, write_header=True)
with open("key", "w") as f:
    f.write(mat.key + '\n')
    f.write(mat2.key + '\n')
