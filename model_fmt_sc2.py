import struct
class FRead(object): #Generic file reader
    def __init__(self,f,big_endian=False):
        self.endian='<'
        if(big_endian):
            self.endian ='>'
        self.file = f
        def swapEndian():
            if(self.endian == '>'):
                self.endian='<'
            else:
                self.endian='>'
        def u32(self):
            return struct.unpack(self.endian+'I', self.file.read(4))[0]
        def u16(self):
            return struct.unpack(self.endian+'H', self.file.read(2))[0]
        def u8(self):
            return struct.unpack(self.endian+'B', self.file.read(1))[0]
        def s32(self):
            return struct.unpack(self.endian+'i', self.file.read(4))[0]
        def s16(self):
            return struct.unpack(self.endian+'h', self.file.read(2))[0]
        def s8(self):
            return struct.unpack(self.endian+'b', self.file.read(1))[0]
        def f16(self):
            return struct.unpack(self.endian+'e', self.file.read(2))[0]
        def f32(self):
            return struct.unpack(self.endian+'f', self.file.read(4))[0]
        def seek(self,offset,whence=0):
            self.file.seek(offset,whence)
        def tell(self):
            self.file.tell()
        def read(self,x):
            self.file.read(x)

        
class VM(object): #Vertex Model, Xbox = X GC = G (Example VMX,VMG so on)
    class Header(object):
        def __init__(self):
            tmpOnC = [0,0] #Intended to quick n dirty offset & count
            self.MAGIC = 'VMX.'
            self.Version = 4
            self.endian = False #False LITTLE, True BIG
            #if(self.Version == 3):#(GC)PPC is Big Endian, (PS2)Mips & (Xbox)x86 is Little Endian
            self.modelContent = 0
            self.MatricesInfo = tmpOnC.copy()
            self.Layer0Info = tmpOnC.copy()
            self.Layer1Info = tmpOnC.copy()
            self.Layer2Info = tmpOnC.copy()
            self.BoneInfo = tmpOnC.copy()
            self.MaterialsInfo = tmpOnC.copy()
            self.MeshCount = 1
            self.TextureTableOffset = 0
            self.TextureMapOffset = 0
            self.ukn_MatrixTableOffset = 0
            self.WeightTableOffset = 0
            self.ukn01_offset = 0
            self.BoneNameOffset = 0
            self.BoneHeaderOffset = 0
        def read(self,f):
            self.MAGIC = f.read(4)
            if(self.MAGIC == 'VMG.'):
                f.swapEndian()
                self.endian = True
            self.Version = f.u8()
            self.modelContent = f.u8()
            self.MatricesInfo[0] = f.u16()
            self.Layer0Info[0] = f.u16()
            self.Layer1Info[0] = f.u16()
            self.Layer2Info[0] = f.u16()
            self.BoneInfo[0] = f.u16()
            self.MaterialsInfo[0] = f.u16()
            self.MeshCount = f.u16()
            self.TextureTableOffset = f.u32()
            self.MaterialsInfo[1] = f.u32()
            self.TextureMapOffset = f.u32()
            self.MatricesInfo[1] = f.u32()
            self.ukn_MatrixTableOffset = f.u32()
            self.Layer0Info[1] = f.u32()
            self.Layer1Info[1] = f.u32()
            self.Layer2Info[1] = f.u32()
            self.WeightTableOffset = f.u32()
            self.ukn01_offset = f.u32()
            self.BoneInfo[1] = f.u32()
            self.BoneNameOffset = f.u32()
            self.BoneHeaderOffset = f.u32()
            



    def __init__(self):
        self.f = None
        self.header = self.Header()
    def read(self,f):
        self.f = FRead(f)
        self.header.read(self.f)