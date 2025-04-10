import model_fmt_sc2
import sys

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)

mdl_file.close()

obj = open(sys.argv[1] + ".obj", "w")



print(str(mdl.header))
totalRigged = 0
currentObj = 0
currentVertH = 1

def triangle_strip_to_list(tri_data):
    #assume tristrip
    triangles = []
    for i in range(len(tri_data) - 2):
        tri_a = tri_data[i]
        tri_b = tri_data[i + 1]
        tri_c = tri_data[i + 2]
        if ((tri_a != tri_b and tri_b != tri_c and tri_c != tri_a) and (tri_a != 0xFFFF and tri_b != 0xFFFF and tri_c != 0xFFFF)):
            if (i % 2 == 0):
                triangles.append((tri_a, tri_b, tri_c))
            else:
                triangles.append((tri_a, tri_c, tri_b))
    return triangles
             

for x in mdl.Object_0:
    match x.ObjectType:
        case 0:
            obj.write(str("o Obj_%02i\n" % currentObj))
            currentObj+=1
            
            for y in x.StaticVerts:
                obj.write(str("v %f %f %f\n"%(y.Position[0],y.Position[1],y.Position[2])))
        case 4:
            obj.write(str("o Obj_%02i\n" % currentObj))
            currentObj+=1
            
            for y in x.RiggedVerts[1]:
                obj.write(str("v %f %f %f\n"%(y.Position[0],y.Position[1],y.Position[2])))
    polygons = triangle_strip_to_list(x.Mesh)
    for pp in polygons:
        obj.write("f")
        for p in pp:
            obj.write(str(" %i" % (p+currentVertH)))
        obj.write("\n")
    currentVertH += len(x.StaticVerts) + len(x.RiggedVerts[1])





'''total = 0
for x in mdl.wgtTbl.VertCounts:
    total += x
print("Total Verts Weghted %i" % total)
'''


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
        