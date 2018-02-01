import sys
import numpy as np
from numpywren.matrix import BigMatrix
import struct
import time

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

cont = True
sleep_time = 0
while cont:
    try:
        time.sleep(sleep_time)
        mat.put_block(blk.T, idx_0, idx_1)
        cont = False
    except Exception as e:
        if sleep_time == 0:
            sleep_time = 1
        else:
            sleep_time *= 2
        print("%d %d failed sleeping for %d and retrying" % (idx_0, idx_1, sleep_time))
