from library import model_fmt_sc2
import sys
import struct

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

idxfix = [1,18,10,14,8,8,10,12,10,22,19,19,22,19,19,17,20,7,20,7,16,3,0,15,2,15,2,11,9,23,23,23,5,12,12,12,5,3,21,9,4,4,4,4]
for x in range(len(mdl.materials)):
    mdl.materials[x].TextureIdx0 = idxfix[x]


#print(mdl.Object_0[0].Possition)

mdl_file = open(sys.argv[2], "wb")

mdl.write(mdl_file)
mdl_file.close()
curtop = 1