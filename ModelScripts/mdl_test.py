from library import model_fmt_sc2
import sys
import struct

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

idxfix = [23,24,10,5,2,25,13,14,1,12,8,3,4,6,6,6,9,0,7,12,20,17,21,11,15,16,16,18,19]
for x in range(len(mdl.materials)):
    mdl.materials[x].TextureIdx0 = idxfix[x]


#print(mdl.Object_0[0].Possition)

mdl_file = open(sys.argv[2], "wb")

mdl.write(mdl_file)
mdl_file.close()
curtop = 1