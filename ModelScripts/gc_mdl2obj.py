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
        triangles.append((tri_a, tri_b, tri_c))
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
    polygons = []
    nextHi = 0
    obj.write(str("o Obj_%02i\n" % currentObj))
    currentObj+=1
    nextHi = len(x.Possition)
    for z in x.Possition:
        y = z
        obj.write(str("v %f %f %f\n" % (y[0],y[1],y[2])))

    
    for z in x.Mesh:
        posTri = []
        for y in z.IdxArr:
            posTri.append(y[0])
            #polygons.extend(triangle_strip_to_list(y[0]))
        polygons.append(triangle_strip_to_list(posTri))
    msh_idx = 0
    for pp in polygons:
        
        for ppp in pp:
            for p in ppp:
                if(msh_idx == 0):
                    obj.write("f")
                obj.write(str(" %i" % (p+currentVertH)))
                msh_idx += 1
                if(msh_idx == 3):
                    obj.write("\n")
                    msh_idx = 0
    currentVertH += nextHi
