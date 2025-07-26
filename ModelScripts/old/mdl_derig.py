#For testing purpuses to get a rig from a model to static mesh to

from library import model_fmt_sc2,sys

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

mdl.header.WeightTableCount = 0
newObjs = []
for x in mdl.Object_0:
    if(x.ObjectType == 4):
        pass
    else:
        newObjs.append(x)
mdl.Object_0 = newObjs
newObjs = []
for x in mdl.Object_1:
    if(x.ObjectType == 4):
        pass
    else:
        newObjs.append(x)
mdl.Object_1 = newObjs
newObjs = []
for x in mdl.Object_2:
    if(x.ObjectType == 4):
        pass
    else:
        newObjs.append(x)
mdl.Object_2 = newObjs

mdl.wgtTbl = mdl.WeightTable()
mdl.header.WeightTableCount = 0

mdl_file = open(sys.argv[2], "wb")
mdl.write(mdl_file)