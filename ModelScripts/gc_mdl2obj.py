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



totalRigged = 0
currentObj = 0


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
    while(next_bone != 255):
        bon = bonez[next_bone]
        d = euler_to_degrees(bon.Rotation[0],bon.Rotation[1],bon.Rotation[2])
        e = degrees_to_radians(d[0],d[1],d[2])
        r = mathutils.Euler((e[0],e[1],e[2]))
        transforms.rotate(r)
        tra = mathutils.Vector((bon.StartPositionXYZScale[0],bon.StartPositionXYZScale[1],bon.StartPositionXYZScale[2]))
        transforms = transforms + tra
        next_bone = bon.BoneParentIdx
    loc = transforms
    return (loc[0],loc[1],loc[2])
def applyTransform_norm(vertex,bone_idx,bonez):
    next_bone = bone_idx
    transforms = mathutils.Vector((vertex[0],vertex[1],vertex[2]))
    while(next_bone != 255):
        bon = bonez[next_bone]
        d = euler_to_degrees(bon.Rotation[0],bon.Rotation[1],bon.Rotation[2])
        e = degrees_to_radians(d[0],d[1],d[2])
        r = mathutils.Euler((e[0],e[1],e[2]))
        transforms.rotate(r)
        next_bone = bon.BoneParentIdx
    loc = transforms
    return (loc[0],loc[1],loc[2])

currentVertHv = 1
currentVertHn = 1
currentVertHt = 1
for x in mdl.Object_0:
    polygonsv = []
    polygonsn = []
    polygonst = []
    obj.write(str("o Obj_%02i\n" % currentObj))
    currentObj+=1
    nextHiv = len(x.PositionStorage.values)
    nextHin = len(x.NormalStorage.values)
    nextHit = len(x.UVStorage.values)
    for z in x.PositionStorage.values:
        y = applyTransform(z,mdl.matrix_table[x.MatrixIndex].ParentBoneIdx,mdl.boneInfo)
        obj.write(str("v %f %f %f\n" % (y[0],y[1],y[2])))
    for z in x.NormalStorage.values:
        y = applyTransform_norm(z,mdl.matrix_table[x.MatrixIndex].ParentBoneIdx,mdl.boneInfo)
        obj.write(str("vn %f %f %f\n" % (y[0],y[1],y[2])))
    for y in x.UVStorage.values:
        obj.write(str("vt %f %f\n" % (y[0],y[1])))

    
    for z in x.Mesh:
        posTri = []
        norTri = []
        texTri = []
        for y in z.IdxArr:
            posTri.append(y[0])
        for y in z.IdxArr:
            norTri.append(y[1])
        for y in z.IdxArr:
            texTri.append(y[3])
        polygonsv.append(triangle_strip_to_list(posTri))
        polygonsn.append(triangle_strip_to_list(norTri))
        polygonst.append(triangle_strip_to_list(texTri))
    flatPie = []
    for x in range(len(polygonsv)):
        v = polygonsv[x]
        n = polygonsn[x]
        t = polygonst[x]
        if(len(v)):
            for y in range(len(v)):
                for z in range(3):
                    flatPie.append((v[y][z],t[y][z],n[y][z]))
    msh_idx = 0
    for pp in flatPie:
        if(msh_idx == 0):
            obj.write("f")
        obj.write(str(" %i/%i/" % ((pp[0]+currentVertHv),(pp[1]+currentVertHt))))
        msh_idx += 1
        if(msh_idx == 3):
            obj.write("\n")
            msh_idx = 0
    currentVertHv += nextHiv
    #currentVertHn += nextHin
    currentVertHt += nextHit
