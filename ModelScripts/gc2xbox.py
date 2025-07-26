from library import model_fmt_sc2
import sys
import struct

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()
mdl.toXbox()

#print(mdl.Object_0[0].Possition)

mdl_file = open(sys.argv[2], "wb")

mdl.write(mdl_file)
mdl_file.close()