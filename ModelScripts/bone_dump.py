import model_fmt_sc2
import sys

import json

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)

mdl_file.close()

mdl_file = open(sys.argv[2], "w")
for x in mdl.boneInfo:
    mdl_file.write(str(x.Name))
    mdl_file.write('\n')
    

mdl_file.close()