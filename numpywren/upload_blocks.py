import sys
import numpy as np
from numpywren.matrix import BigMatrix
import struct

with open("key", "r") as f:
    key = f.readline().strip() + ".out"
with open("shape", "r") as f:
    N = int(f.readline().strip())
    NB = int(f.readline().strip())
idx_0 = int(sys.argv[1])
idx_1 = int(sys.argv[2])
print("UPLOADING %d %d" % (idx_0, idx_1))
mat = BigMatrix(key, shape=[N, N+1000], shard_sizes=[NB, NB], write_header=True)
with open("/dev/shm/%d_%d" % (idx_0, idx_1), "rb") as f:
    MB = struct.unpack('i', f.read(4))[0]
    NB = struct.unpack('i', f.read(4))[0]
    blk = np.fromstring(f.read())
    # NB and MB intentionally switched
    blk = blk.reshape([NB, MB])
mat.put_block(blk.T, idx_0, idx_1)
