import sys
from library import model_fmt_sc2
import copy

host = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(host)
host.close()

slave = open(sys.argv[2], "rb")

ps2 = model_fmt_sc2.FRead(slave)
ps2.seek(10)
bonecount = ps2.u16()
ps2.seek(0x10)
boneoffset = ps2.u32()
ps2.seek(boneoffset)
readr = model_fmt_sc2.FRead(ps2)
bones = []
for x in range(bonecount):
    bon = model_fmt_sc2.VM.BoneInfo()
    bon.read(readr,False)
    bones.append(bon)



slave.close()

mdl.boneInfo = copy.deepcopy(bones)

output = open(sys.argv[3], "wb")
mdl.write(output)
output.close()