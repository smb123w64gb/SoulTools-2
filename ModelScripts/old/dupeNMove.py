from library import model_fmt_sc2
import sys
import struct
import copy

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

clone = copy.deepcopy(mdl.Object_0[0])
for x in clone.StaticVerts:
    x.Position = [x.Position[0]*2.0,x.Position[1]*2.0,x.Position[2]*2.0]
mdl.Object_0.append(clone)

mdl_file = open(sys.argv[2], "wb")
mdl.write(mdl_file)