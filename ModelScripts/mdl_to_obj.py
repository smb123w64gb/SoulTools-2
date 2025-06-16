import model_fmt_sc2
import sys
import mathutils

import math

def euler_to_degrees(roll, pitch, yaw):
    roll_deg = float(roll) * 360.0
    pitch_deg = float(pitch)* 360.0
    yaw_deg = float(yaw)* 360.0
    return roll_deg, pitch_deg, yaw_deg

def degrees_to_radians(roll, pitch, yaw):
    roll_rad = float(roll) * (math.pi / 180.0)
    pitch_rad = float(pitch) * (math.pi / 180.0)
    yaw_rad = float(yaw) * (math.pi / 180.0)
    return roll_rad, pitch_rad, yaw_rad

def radians_to_degrees(roll, pitch, yaw):
    roll_rad = 180.0 * float(roll) / (math.pi)
    pitch_rad = 180.0 * float(pitch) / (math.pi)
    yaw_rad = 180.0 * float(yaw) / (math.pi)
    return roll_rad, pitch_rad, yaw_rad

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
             
def applyTransform(vertex,bone_idx,bonez):
    next_bone = bone_idx
    transforms = mathutils.Vector((vertex[0],vertex[1],vertex[2]))
    chain = []
    while(next_bone != 255):
        bon = bonez[next_bone]
        d = euler_to_degrees(bon.Rotation[0],bon.Rotation[1],bon.Rotation[2])
        e = degrees_to_radians(d[0],d[1],d[2])
        r = mathutils.Euler((e[0],e[1],e[2]))
        transforms.rotate(r)
        tra = mathutils.Vector((bon.StartPositionXYZScale[0],bon.StartPositionXYZScale[1],bon.StartPositionXYZScale[2]))
        transforms = transforms + tra
        chain.append(next_bone)
        next_bone = bon.BoneParentIdx
    loc = transforms
    return (loc[0],loc[1],loc[2])


for x in mdl.Object_0:
    nextHi = 0
    match x.ObjectType:
        case 0:
            obj.write(str("o Obj_%02i\n" % currentObj))
            currentObj+=1
            nextHi = len(x.StaticVerts)
            for z in x.StaticVerts:
                y = applyTransform(z.Position,mdl.matrix_table[x.MatrixIndex].ParentBoneIdx,mdl.boneInfo)
                obj.write(str("v %f %f %f\n"%(y[0],y[1],y[2])))
        case 4:
            pass
            obj.write(str("o Obj_%02i\n" % currentObj))
            currentObj+=1
            nextHi = len(x.RiggedVerts[1])
            for y in x.RiggedVerts[1]:

                obj.write(str("v %f %f %f\n"%(y.Position[0],y.Position[1],y.Position[2])))
    polygons = triangle_strip_to_list(x.Mesh)
    for pp in polygons:
        obj.write("f")
        for p in pp:
            obj.write(str(" %i" % (p+currentVertH)))
        obj.write("\n")
    currentVertH += nextHi
