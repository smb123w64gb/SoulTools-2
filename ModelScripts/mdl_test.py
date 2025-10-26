from library import model_fmt_sc2
import sys
import struct

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

idxfix = [0,23,3,2,19,4,15,14,8,7,6,5,29,28,25,11,27,13,26,10,12,18,17,9,20,1,24,22,21,16,6,29]
for x in range(len(mdl.materials)):
    mdl.materials[x].TextureIdx0 = idxfix[x]


#print(mdl.Object_0[0].Possition)

mdl_file = open(sys.argv[2], "wb")

mdl.write(mdl_file)
mdl_file.close()
curtop = 1