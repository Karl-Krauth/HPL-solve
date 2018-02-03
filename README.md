# HPL-solve
Update the key file in `numpywren/key` and set the lambda parameter in `numpywren/download_block.py` and the output key in `numpywren/upload_block.py`
Judge Karl for making the configuration so convoluted, push your changes and run:
```cp ec2standalone.cloudinit.template ~/pywren/pywren/ec2_standalone_files/
```
```pywren standalone launch_instances 50  --pywren_git_branch=standalone-multiple-executors --spot_price=3.
```
Run the below command with `INSTANCE_PROFILE_NAME` set to the value configured in your .pywren\_config
```sudo bash broadcast_nodes INSTANCE_PROFILE_NAME
```
ssh into any of your nodes and run:
```mpirun -n 2400 -ppn 48 -f ~/nodefile ~/HPL-solve/hpl-2.2/bin/ec2/xhpl > res.out```
