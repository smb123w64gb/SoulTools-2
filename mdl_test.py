import model_fmt_sc2
import sys

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
for bones in mdl.boneInfo:
    print(bones.Name)