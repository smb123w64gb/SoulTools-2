import sys
import model_fmt_sc2
import copy

host = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(host)
host.close()

slave = open(sys.argv[2], "rb")

mdl_s = model_fmt_sc2.VM()

mdl_s.read(slave)
slave.close()

mdl.boneInfo = copy.deepcopy(mdl_s.boneInfo)

bonemax = len(mdl.boneInfo)-1
for x in mdl.wgtTbl.WeightBuffer:
    for y in x:
        if(y.bIdx > bonemax):
            y.bIdx = bonemax

output = open(sys.argv[3], "wb")
mdl.write(output)
output.close()