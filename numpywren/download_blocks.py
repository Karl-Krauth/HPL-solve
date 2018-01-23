import sys
from numpywren.matrix import BigMatrix
import numpy as np

with open("key", "r") as f:
    key = f.readline().strip()
    # B_key = f.readline().strip()
idx_0 = int(sys.argv[1])
idx_1 = int(sys.argv[2])
print("GETTING " + str(idx_0) + "," + str(idx_1))
def fn(bigm, *block_idx):
    real_idss = bigm.__block_idx_to_real_idx__(block_idx)
    current_shape = tuple([e - s for s,e in real_idss])
    mat = np.random.rand(current_shape[0], current_shape[1])
    bigm.put_block(mat, *block_idx)
    return mat
mat = BigMatrix(key, parent_fn=fn)
# B = BigMatrix(B_key)
with open("shape", "w") as f:
    f.write("%d\n" % mat.shape[0])
    f.write("%d\n" % mat.shard_sizes[0])

blk = mat.get_block(idx_0, idx_1)
"""
start_idx = idx_1 * mat.shard_sizes[0]
end_idx = (idx_1 + 1) * mat.shard_sizes[0]
num_blocks = ((mat.shape[0] + (mat.shard_sizes[0] - 1)) // mat.shard_sizes[0])
if end_idx <= mat.shape[0]:
    blk = mat.get_block(idx_0, idx_1)
elif start_idx >= mat.shape[0]:
    blk = B.get_block(idx_0, idx_1 - num_blocks)
else:
    blk = A.get_block( 
"""
with open("/dev/shm/%d_%d" % (idx_0, idx_1), "wb") as f:
    f.write(blk.T.tobytes())
