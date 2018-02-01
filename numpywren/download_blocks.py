import sys
from numpywren.matrix import BigMatrix, BigSymmetricMatrix
import numpy as np

with open("key", "r") as f:
    key = f.readline().strip()
    B_key = f.readline().strip()
idx_0 = int(sys.argv[1])
idx_1 = int(sys.argv[2])
N = 1281167
NB = 4096
print("GETTING " + str(idx_0) + "," + str(idx_1))
mat = BigSymmetricMatrix(key, shape=[N, N], shard_sizes=[NB, NB], lambdav=1e-4)
B = BigMatrix(B_key, shape=[N, 1000], shard_sizes=[NB, 1000])
with open("shape", "w") as f:
    f.write("%d\n" % mat.shape[0])
    f.write("%d\n" % mat.shard_sizes[0])

start_idx = idx_1 * mat.shard_sizes[0]
end_idx = (idx_1 + 1) * mat.shard_sizes[0]
num_blocks = ((mat.shape[0] + (mat.shard_sizes[0] - 1)) // mat.shard_sizes[0])
if end_idx <= mat.shape[0]:
    blk = mat.get_block(idx_0, idx_1)
elif start_idx >= mat.shape[0]:
    blk = B.get_block(idx_0, idx_1 - num_blocks)
    last_col_len = (mat.shape[1] + B.shape[1]) % mat.shard_sizes[1]
    blk = blk[:, -last_col_len:]
elif start_idx < mat.shape[0] and end_idx > mat.shape[0]:
    blk = mat.get_block(idx_0, idx_1)
    blk2 = B.get_block(idx_0, 0)
    blk = np.append(blk, blk2, axis=1)
    if blk.shape[1] > mat.shard_sizes[0]:
        blk = blk[:, :mat.shard_sizes[0]]
else:
    # TODO ensure we account for aligning
    assert(False) 
with open("/dev/shm/%d_%d" % (idx_0, idx_1), "wb") as f:
    f.write(blk.T.tobytes())
