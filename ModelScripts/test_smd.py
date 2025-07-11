import sys
import smd_lib

obj = open(sys.argv[1], "r")

inModel = smd_lib.SMD()
inModel.read(obj)
for x,idx in inModel.mesh_original.items():
    x:smd_lib.SMD.MVXT = idx
    x.sort()
    print(x.poly())
    #print(x.idxs)