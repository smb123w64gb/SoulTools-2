import texture_fmt_sc2
import sys,os,struct

vxt_file = open(sys.argv[1], "rb")

newTex = texture_fmt_sc2.VTX()
newTex.read(vxt_file)
vxt_file.close()

vxt_file = open(sys.argv[1], "wb")
newTex.write(vxt_file)
vxt_file.close()