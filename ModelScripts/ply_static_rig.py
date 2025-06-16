import sys
import model_fmt_sc2
import copy
import os
import mathutils



class Model(object):
    def __init__(self):
        self.verts = []
        self.norms = []
        self.texcr = []
        self.color = []

        self.poly = []
    def readVert(self,v):
        self.verts.append([float(v[0]),float(v[1]),float(v[2])])
        self.norms.append([float(v[3]),float(v[4]),float(v[5])])
        self.color.append([int(v[6]),int(v[7]),int(v[8]),int(v[9])])
        self.texcr.append([float(v[10]),float(v[11])])
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
bone_idxes_fixup = [3,1,12,13,14,15,17,18,19,4,6,7,8,10,11]

def applyTransform(vertex,bone_idx,bonez):
    fin_trans = [0.0,0.0,0.0]
    fin_rot = [0.0,0.0,0.0]
    next_bone = bone_idx
    while(next_bone != 255):
        bon = bonez[next_bone]
        fin_trans = [fin_trans[0]+bon.StartPositionXYZScale[0],fin_trans[1]+bon.StartPositionXYZScale[1],fin_trans[2]+bon.StartPositionXYZScale[2]]
        fin_rot = [fin_rot[0]+bon.Rotation[0],fin_rot[1]+bon.Rotation[1],fin_rot[2]+bon.Rotation[2]]
        next_bone = bon.BoneParentIdx

    transform = [vertex[0]-fin_trans[0], vertex[1]-fin_trans[1], vertex[2]-fin_trans[2]]

    return transform

mdl_file = open(sys.argv[2], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()



newmat = copy.deepcopy(mdl.materials[0])
newmat.TextureIdx0 = 0
newmat.TextureIdx1 = None
newmat.TextureIdx2 = None
mdl.materials[0] = newmat
mdl.materials = mdl.materials[:1]

mdl.Object_0 = []
for idx,x in enumerate(ply_mdls):
    mdl_lay = x.toVMX()
    #for y in mdl_lay.StaticVerts:
    #    y.Position = applyTransform(y.Position,bone_idxes_fixup[idx],mdl.boneInfo)
    mdl_lay.MaterailIndex = 0
    mdl_lay.MatrixIndex = bone_idxes_fixup[idx]
    mdl.Object_0.append(mdl_lay)


mdl_file = open(sys.argv[3], "wb")
mdl.write(mdl_file)