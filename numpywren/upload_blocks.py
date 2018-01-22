import sys
import numpy as np
from numpywren.matrix import BigMatrix

with open("key", "r") as f:
    key = f.readline().strip() + ".out"
with open("shape", "r") as f:
    N = int(f.readline().strip())
    NB = int(f.readline().strip())
idx_0 = int(sys.argv[1])
idx_1 = int(sys.argv[2])
print("UPLOADING %d %d" % (idx_0, idx_1))
mat = BigMatrix(key, shape=[N, N+10], shard_sizes=[NB, NB], write_header=True)
with open("/home/ec2-user/%d_%d" % (idx_0, idx_1), "rb") as f:
    blk = np.fromstring(f.read())
    blk = blk.reshape([blk.shape[0] // NB, NB])
    print(blk.T)
mat.put_block(blk.T, idx_0, idx_1)
print("SUCCESS", idx_0, idx_1)
