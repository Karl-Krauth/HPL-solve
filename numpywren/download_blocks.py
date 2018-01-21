import sys
from numpywren.matrix import BigMatrix

with open("key", "r") as f:
    key = f.readline().strip()
idx_0 = int(sys.argv[1])
idx_1 = int(sys.argv[2])
print("GETTING " + str(idx_0) + "," + str(idx_1))
mat = BigMatrix(key)
with open("shape", "w") as f:
    f.write("%d\n" % mat.shape[0])
    f.write("%d\n" % mat.shard_sizes[0])
blk = mat.get_block(idx_0, idx_1)
with open("/home/ec2-user/%d_%d" % (idx_0, idx_1), "wb") as f:
    print(blk)
    f.write(blk.T.tobytes())
