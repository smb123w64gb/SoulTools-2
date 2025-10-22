import sys
from library import smd_lib
from library import model_fmt_sc2 as sc2m
import mathutils
import copy

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

def fixBone3(vertex):
    loc = mathutils.Vector((vertex[0],vertex[1],vertex[2]))
    mat_rotY = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
    mat_rotZ = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
    mat_rotate = (mat_rotY @ mat_rotZ)
    mat_rotate.invert()
    loc.rotate(mat_rotate)
    return (loc[0],loc[1],loc[2])





def applyTransform(vertex,bone_idx,bonez):
    next_bone = bone_idx
    transforms = mathutils.Vector((vertex[0],vertex[1],vertex[2]))
    chain = []
    while(next_bone != 255):
        bon = bonez[next_bone]
        
        chain.append(next_bone)
        next_bone = bon.BoneParentIdx
    chain.reverse()
    onceler = True
    for x in chain:
        bon = bonez[x]
        
        d = euler_to_degrees(bon.Rotation[0],bon.Rotation[1],bon.Rotation[2])
        e = degrees_to_radians(d[0],d[1],d[2])
        e = [x for x in e]
        r = mathutils.Euler((e[0],e[1],e[2]))
        r = r.to_matrix()
        if(bon.boneType == 3 and onceler):
            mat_rotY = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
            mat_rotZ = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
            mat_rotate = (mat_rotY @ mat_rotZ)
            onceler = False
            r.rotate(mat_rotate)
        r.invert()
        
        tra = mathutils.Vector((-bon.StartPositionXYZScale[0],-bon.StartPositionXYZScale[1],-bon.StartPositionXYZScale[2]))
        transforms = transforms + tra
        transforms.rotate(r)
        
    loc = transforms
    return (loc[0],loc[1],loc[2])
def applyTransform_norm(vertex,bone_idx,bonez):
    next_bone = bone_idx
    transforms = mathutils.Vector((vertex[0],vertex[1],vertex[2]))
    chain = []
    while(next_bone != 255):

           
        bon = bonez[next_bone]
        
        chain.append(next_bone)
        next_bone = bon.BoneParentIdx
    chain.reverse()
    onceler = True
    for x in chain:
        bon = bonez[x]
        
        d = euler_to_degrees(bon.Rotation[0],bon.Rotation[1],bon.Rotation[2])
        e = degrees_to_radians(d[0],d[1],d[2])
        e = [x for x in e]
        r = mathutils.Euler((e[0],e[1],e[2]))
        r = r.to_matrix()
        if(bon.boneType == 3 and onceler):
            mat_rotY = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
            mat_rotZ = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
            mat_rotate = (mat_rotY @ mat_rotZ)
            onceler = False
            r.rotate(mat_rotate)
        r.invert()
        transforms.rotate(r)
        
    loc = transforms
    return (loc[0],loc[1],loc[2])


obj = open(sys.argv[1], "r")

class VXTProto(object):
        def __init__(self):
            self.pos = [0.0]*3
            self.nor = [0.0]*3
            self.uvs = [0.0]*2
            self.wght = 1.0 
            self.idx = 0
        def __str__(self):
             rt = ''
             rt += str("POS:%f,%f,%f\n"%(self.pos[0],self.pos[1],self.pos[2]))
             rt += str("NOR:%f,%f,%f\n"%(self.nor[0],self.nor[1],self.nor[2]))
             rt += str("UVS:%f,%f\n"%(self.uvs[0],self.uvs[1]))
             rt += str("WGT:%f\n"%(self.wght))
             return rt
        def __repr__(self):
             return self.__str__()

inModel = smd_lib.SMD()
inModel.read(obj)
inModel.sort()
for x in inModel.mesh_original.keys():
    print(x.replace('\n',''))

    
mesh = []



mdl_file = open(sys.argv[2], "rb")

mdl = sc2m.VM()

mdl.read(mdl_file)
mdl_file.close()
riggedBuff = []
staticBuffPOSNOR = []
staticBuffUVSCOL = []

boneindx = {}
for x in mdl.boneInfo:
    if(x.BoneNameOffset>0):
        boneindx[x.Name] = x

for idy,y in inModel.merged_list.items():
    binds = {}
    vtnr = sc2m.VM.WeightTable.BufferScaleVertex()
    vtnr.Position = applyTransform(y.pos,0,mdl.boneInfo)
    vtnr.Normal = applyTransform_norm(y.nor,0,mdl.boneInfo)
    staticBuffPOSNOR.append(vtnr)

    uvcl = sc2m.VM.WeightTable.BufferColorUV()
    uvcl.UV = y.uvs
    staticBuffUVSCOL.append(uvcl)
    
    for idz,z in y.bns.items():
            vt = VXTProto()
            vt.pos = y.pos
            vt.nor = y.nor
            vt.uvs = y.uvs
            vt.wght = z
            for bidx,b in enumerate(mdl.boneInfo):
                if b.BoneIdx == boneindx[idz]:
                    vt.idx = bidx

            binds[idz] = vt
    riggedBuff.append(binds)

mdl.wgtTbl.VertexBuff0 = staticBuffUVSCOL
mdl.wgtTbl.VertexBuff1 = staticBuffPOSNOR
mdl.wgtTbl.VertexBuff2 = staticBuffPOSNOR

mdl.matrix_table = mdl.matrix_table[:1]
mdl.materials = mdl.materials[:1]
mdl.materials[0].TextureIdx0 = 0
mdl.materials[0].TextureIdx1 = None
mdl.materials[0].TextureIdx2 = None
material_base = copy.deepcopy(mdl.materials[0])
material_base.TextureMap1 = None
mdl.materials = []
mdl.Object_0 = []
mdl.Object_1 = []
mdl.Object_2 = []

txIndx = 0
for xx,idx in inModel.mesh_original.items():
    x:smd_lib.SMD.MVXT = idx
    mesh = x.poly(inModel.merged_list)
    newlayer = sc2m.VM.LayerObjectEntryXbox()
    newlayer.Mesh = mesh
    newlayer.ObjectType = 4
    newlayer.PrimitiveType = 1
    mat = copy.deepcopy(material_base)
    mdl.materials.append(mat)
    newlayer.MaterialIndex = txIndx
    txIndx += 1
    mdl.Object_0.append(newlayer)






finalPosWgt = []
curhigh = 1
topfour = 4
curIdx = 0
wgtz = []
weghtsub = []
for xx in riggedBuff:
    if(len(xx)>topfour):
        #BindCOunt / CurVtx / SubVertex
        finalPosWgt[-1][-1][-1].stat = 1
        topfour += 1
    elif(curhigh<len(xx)):
        if(curhigh==4):
            pass
        else:
            if(len(weghtsub)):
                finalPosWgt.append(weghtsub)
            weghtsub = []
            curhigh += 1
    wgtz = []
    for idx,x in xx.items():
        
        bone = boneindx[idx]
        updatedPos = applyTransform(x.pos,x.idx,mdl.boneInfo)
        updatedNor = applyTransform_norm(x.nor,x.idx,mdl.boneInfo)
        if(len(xx)>1):
            updatedPos = [(updatedPos[0]*x.wght),(updatedPos[1]*x.wght),(updatedPos[2]*x.wght)]
        wgt = sc2m.VM.WeightTable.WeightDef()
        wgt.Pos = updatedPos
        wgt.Nor = updatedNor
        wgt.bWgt = x.wght
        wgt.bIdx = x.idx
        wgtz.append(wgt)
    weghtsub.append(wgtz)
finalPosWgt.append(weghtsub)
if(curhigh==4):
    finalPosWgt[-1][-1][-1].stat = 4


flatbuffer = []
totalry = [0,0,0,0]
idx = 0
for x in finalPosWgt:
    buf = []
    for y in x:
        totalry[idx] += 1
        for z in y:
            buf.append(z)
    idx+=1
    flatbuffer.append(buf)
mdl.wgtTbl.VertCounts = totalry
mdl.wgtTbl.WeightBuffer = flatbuffer
mdl.header.WeightTableCount = 1

mdl_file = open(sys.argv[3], "wb")

mdl.write(mdl_file)
mdl_file.close()