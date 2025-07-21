import model_fmt_sc2
import sys
import struct

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

idxfix = [0,1,2,1,3,4]
for x in len(mdl.materials):
    mdl.materials[x].TextureIdx0 = idxfix[x]


#print(mdl.Object_0[0].Possition)

mdl_file = open(sys.argv[2], "wb")

mdl.write(mdl_file)
mdl_file.close()
curtop = 1