import model_fmt_sc2
import sys
import struct

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
'''mdl_file.seek(0)

mdlOut = open(sys.argv[1] + "mod.vmx", "wb")
mdlOut.write(mdl_file.read()) #copy the file

mdl_file.close()

boneMax = len(mdl.boneInfo) - 1

mdlOut.seek(0x6)
mdlOut.write(struct.pack('B',1))


mdlOut.seek(mdl.wgtTbl.WeightBufferOffset)

for x in mdl.wgtTbl.WeightBuffer1:
    x.bIdx = 0
    mdlOut.write(x.as_bytes())
for x in mdl.wgtTbl.WeightBuffer2:
    x.bIdx = 0
    mdlOut.write(x.as_bytes())
for x in mdl.wgtTbl.WeightBuffer3:
    x.bIdx = 0
    mdlOut.write(x.as_bytes())
for y in mdl.wgtTbl.WeightBuffer4:
    for x in y:
        x.bIdx = 0
        mdlOut.write(x.as_bytes())


''''''

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
'''