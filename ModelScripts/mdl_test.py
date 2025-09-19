from library import model_fmt_sc2
import sys
import struct

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

idxfix = [7,21,4,26,23,13,22,6,15,3,18,6,9,17,19,12,2,11,1,5,0,11,10,20,8,24,14,25,16]
for x in range(len(mdl.materials)):
    mdl.materials[x].TextureIdx0 = idxfix[x]


#print(mdl.Object_0[0].Possition)

mdl_file = open(sys.argv[2], "wb")

mdl.write(mdl_file)
mdl_file.close()
curtop = 1