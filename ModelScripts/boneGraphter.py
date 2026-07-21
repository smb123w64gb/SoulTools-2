import sys
from library import model_fmt_sc2
import copy

host = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(host)
host.close()

slave = open(sys.argv[2], "rb")

mdl_s = model_fmt_sc2.VM()

mdl_s.read(slave)
slave.close()

boneCopy = copy.deepcopy(mdl_s.boneInfo)
boneIn = copy.deepcopy(mdl.boneInfo)

curBone = len(boneIn)
fixb : model_fmt_sc2.VM.BoneInfo =  boneCopy[171]
fixb.BoneIdx = curBone
boneIn.append(fixb)
curBone = len(boneIn)
fixb : model_fmt_sc2.VM.BoneInfo =  boneCopy[178]
fixb.BoneIdx = curBone
fixb.BoneParentIdx = curBone-1
boneIn.append(fixb)
curBone = len(boneIn)
fixb : model_fmt_sc2.VM.BoneInfo = boneCopy[183]
fixb.BoneIdx = curBone 
fixb.BoneParentIdx = curBone-1
boneIn.append(fixb)
curBone = len(boneIn)
fixb : model_fmt_sc2.VM.BoneInfo =  boneCopy[184]
fixb.BoneIdx = curBone 
fixb.BoneParentIdx = curBone-1
boneIn.append(fixb)
for idx,x in enumerate(boneIn):
    print("Bone IDX %03i : %03i : P %03i : %s" %(idx,x.BoneIdx,x.BoneParentIdx,x.Name))



mdl.boneInfo = copy.deepcopy(boneIn)


output = open(sys.argv[3], "wb")
mdl.write(output)
output.close()
