import model_fmt_sc2
import sys

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)

mdl_file.close()

print(str(mdl.header))
totalRigged = 0

for x in mdl.Object_2:
    if(x.ObjectType == 4):
        x.




total = 0
for x in mdl.wgtTbl.VertCounts:
    total += x
print("Total Verts Weghted %i" % total)

'''
obj = open(sys.argv[1] + ".obj", "w")

weght = 0.0
idxs = []

obj.write("o test\n")

for x in mdl.wgtTbl.WeightBuffer1:
    obj.write(str("v %f %f %f\n" % (x.Pos[0],x.Pos[1],x.Pos[2])))
for x in mdl.wgtTbl.WeightBuffer2:
    obj.write(str("v %f %f %f\n" % (x.Pos[0],x.Pos[1],x.Pos[2])))
for x in mdl.wgtTbl.WeightBuffer3:
    obj.write(str("v %f %f %f\n" % (x.Pos[0],x.Pos[1],x.Pos[2])))
for y in mdl.wgtTbl.WeightBuffer4:
    for x in y:
        obj.write(str("v %f %f %f\n" % (x.Pos[0],x.Pos[1],x.Pos[2])))
'''
'''for x in mdl.wgtTbl.WeightBuffer4:
    idxs.append(str("%i : %.2f"%(x.bIdx,x.bWgt)))
    weght += x.bWgt
    if(weght>.999999):
        print("%s Count %i"%(str(idxs), len(idxs)))
        print(weght)
        idxs = []
        weght = 0.0'''
        