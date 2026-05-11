import sys
from library import model_fmt_sc2
import copy
import os
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


class Model(object):
    def __init__(self):
        self.verts = []
        self.norms = []
        self.texcr = []
        self.color = []
        self.boneIdx = 0

        self.poly = []
    def readVert(self,v):
        if(len(v)>11):
            self.verts.append([float(v[0]),float(v[1]),float(v[2])])
            self.norms.append([float(v[3]),float(v[4]),float(v[5])])
            self.color.append([int(v[6]),int(v[7]),int(v[8]),int(v[9])])
            self.texcr.append([float(v[10]),float(v[11])])
        else:
            self.verts.append([float(v[0]),float(v[1]),float(v[2])])
            self.norms.append([float(v[3]),float(v[4]),float(v[5])])
            self.color.append([int(255),int(255),int(255),int(255)])
            self.texcr.append([float(v[6]),float(v[7])])
    def readPoly(self,v):
        self.poly.append([int(v[1]),int(v[2]),int(v[3])])
    def toVMX(self):
        newOBJ = model_fmt_sc2.VM().LayerObjectEntryXbox()
        flatPoly = []
        for x in self.poly:
            for y in x:
                flatPoly.append(y)
        newOBJ.Mesh = flatPoly
        static_arr = []
        for x in range(len(self.verts)):
            vx = model_fmt_sc2.VM().LayerObjectEntryXbox().BufferStaticVertex()
            vx.Position = self.verts[x]
            vx.Normal = self.norms[x]
            vx.RGBA = self.color[x]
            vx.UV = self.texcr[x]
            static_arr.append(vx)
        newOBJ.StaticVerts = static_arr
        newOBJ.PrimitiveType = 1
        return newOBJ 
mdl_file = open(sys.argv[2], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()
ply_mdls = []
files = os.listdir(sys.argv[1])
files = [ fi for fi in files if fi.lower().endswith(".ply") ]
for y in files:
    obj_file = open(sys.argv[1] + '\\' + y, "r")
    vertCount = 0
    polyCount = 0
    start_read = False
    mdl_txt = Model()
    boneLoc = y.lower().find(".ply")
    lenStr = len(y) - boneLoc
    BoneName = y[0:len(y)-4]
    results = [item for item in mdl.boneInfo if item.Name == BoneName]
    mdl_txt.boneIdx = results[0].BoneIdx
    print(BoneName)
    for x in obj_file.readlines():
        if(start_read):
            if(vertCount):
                mdl_txt.readVert(x.split())
                vertCount -= 1
            elif(polyCount):
                mdl_txt.readPoly(x.split())
                polyCount -= 1
        if(x.find('element vertex ') == 0):
            vertCount = int(x.split()[-1])
        if(x.find('element face ') == 0):
            polyCount = int(x.split()[-1])
        if(x.find('end_header')==0):
            start_read = True
    ply_mdls.append(mdl_txt)
texturefix = [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0]

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
        if(bon.boneType == 3 and False):
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
        if(bon.boneType == 3 and False):
            mat_rotY = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
            mat_rotZ = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
            mat_rotate = (mat_rotY @ mat_rotZ)
            onceler = False
            r.rotate(mat_rotate)
        r.invert()
        transforms.rotate(r)
        
    loc = transforms
    return (loc[0],loc[1],loc[2])



#get our matrixes up
cloned_matrix = copy.deepcopy(mdl.matrix_table[0])

new_matrixes = []

for indx,x in enumerate(mdl.boneInfo):
    if(len(x.Name)>0):
        clean = copy.copy(cloned_matrix)
        clean.Type = 2
        clean.ParentBoneIdx = indx
        new_matrixes.append(clean)

mdl.matrix_table = new_matrixes


newmat = copy.deepcopy(mdl.materials[0])
newmat.TextureIdx0 = 0
newmat.TextureIdx1 = None
newmat.TextureIdx2 = None
newmat.Type = 3
newmat.OpacitySrc = 1
#newmat.CullMode = 0
#mdl.materials[0] = newmat
#mdl.materials = mdl.materials[:1]


mdl.Object_0 = []
mdl.Object_1 = []
mdl.Object_2 = []
mdl.materials = []
mdl.wgtTbl = mdl.WeightTable()
mdl.header.WeightTableCount = 0
for idx,x in enumerate(ply_mdls):
    mdl_lay = x.toVMX()
    curmat = copy.deepcopy(newmat)
    for y in mdl_lay.StaticVerts:
        y.Position = applyTransform(y.Position,x.boneIdx,mdl.boneInfo)
        y.Normal = applyTransform_norm(y.Normal,x.boneIdx,mdl.boneInfo)
    curmat.TextureIdx0 = texturefix[idx]
    curmat.OpacitySrc += texturefix[idx]
    mdl.materials.append(curmat)
    mdl_lay.MaterialIndex = idx
    mdl_lay.MatrixIndex = x.boneIdx
    if(texturefix[idx]):
        mdl.Object_1.append(mdl_lay)
    else:
        mdl.Object_0.append(mdl_lay)


mdl_file = open(sys.argv[3], "wb")
mdl.write(mdl_file)
mdl_file.close()