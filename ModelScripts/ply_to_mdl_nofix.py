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

ply_mdls = []
files = os.listdir(sys.argv[1])
files = [ fi for fi in files if fi.lower().endswith(".ply") ]
for y in files:
    obj_file = open(sys.argv[1] + '\\' + y, "r")
    vertCount = 0
    polyCount = 0
    start_read = False
    mdl_txt = Model()
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
bone_idxes_fixup = [0,0,1,2,3,6,7]


mdl_file = open(sys.argv[2], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

#get our matrixes up
cloned_matrix = copy.deepcopy(mdl.matrix_table[0])

new_matrixes = []

for idx,x in enumerate(mdl.boneInfo):
    if(len(x.Name)>0):
        clean = copy.copy(cloned_matrix)
        clean.Type = 2
        clean.ParentBoneIdx = idx
        new_matrixes.append(clean)

mdl.matrix_table = new_matrixes




mdl.Object_0 = []
mdl.Object_1 = []
mdl.Object_2 = []
mdl.wgtTbl = mdl.WeightTable()
mdl.header.WeightTableCount = 0
for idx,x in enumerate(ply_mdls):
    mdl_lay = x.toVMX()
    mdl_lay.MaterailIndex = 0
    mdl_lay.MatrixIndex = bone_idxes_fixup[idx]
    mdl.Object_0.append(mdl_lay)


mdl_file = open(sys.argv[3], "wb")
mdl.write(mdl_file)