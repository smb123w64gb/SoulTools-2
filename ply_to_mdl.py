import sys
import model_fmt_sc2
import copy

obj_file = open(sys.argv[1], "r")

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



mdl_file = open(sys.argv[2], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

mdl_file = open(sys.argv[3], "wb")

newmat = copy.deepcopy(mdl.materials[0])
newmat.TextureIdx0 = 2
mdl.materials.append(newmat)
mdl_lay = mdl_txt.toVMX()

mdl_lay.MaterailIndex = 2
mdl.Object_0[1] = mdl_lay
mdl.write(mdl_file)




    