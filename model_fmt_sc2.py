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
    def f32_4(self):
        return struct.unpack(self.endian+'ffff', self.file.read(16))[0:4]
    def f32_3(self):
        return struct.unpack(self.endian+'fff', self.file.read(12))[0:3]
    def seek(self,offset,whence=0):
        self.file.seek(offset,whence)
    def tell(self):
        self.file.tell()
    def read(self,x):
        return self.file.read(x)
    def getString(self,offset = 0):
        if(offset):
            ret = self.file.tell()
            self.seek(offset)
        result = ""
        tmpChar = self.file.read(1)
        while ord(tmpChar) != 0:
            result += tmpChar.decode("utf-8")
            tmpChar = self.file.read(1)
        if(offset):
            self.seek(ret)
        return result
class MTX(object):
    def __init__(self):
        self.matrix = [[0.0,0.0,0.0,0.0]*4]
    def read(self,f):
        tmp = []
        for x in range(4):
            tmp.append(f.f32_4())
        self.matrix = tmp
class VM(object): #Vertex Model, Xbox = X GC = G (Example VMX,VMG so on)
    class Header(object):
        def __init__(self):
            tmpOnC = [0,0] #Intended to quick n dirty offset & count
            self.MAGIC = 'VMX.'
            self.Version = 4
            self.Endian = False #False LITTLE, True BIG
            #if(self.Version == 3):#(GC)PPC is Big Endian, (PS2)Mips & (Xbox)x86 is Little Endian
            self.ModelContent = 0
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
                self.Endian = True
            self.Version = f.u8()
            f.seek(4,1)
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
    class MatrixUnk(object):
        def __init__(self):
            self.unk = 0
            self.Count = 0
            self.Offset = 0
        def read(self,f):
            self.unk = f.u16()
            self.Count = f.u16()
            self.Offset = f.u32()
    class MatrixTable(object):
        def __init__(self):
            self.Type = 0
            self.ParentBoneIdx = 0
            self.unk1 = 0
            self.unk2 = 0 #stage file thingy
            self.unk3 = 0
            self.unk4 = 0
            self.Matrix = MTX()
        def read(self,f):
            self.Type = f.u8()
            self.ParentBoneIdx = f.u8()
            self.unk1 = f.u16()
            self.unk2 = f.u32()
            self.unk3 = f.u32()
            self.unk4 = f.u32()
            self.Matrix.read(f)
    class BoneInfo(object):
        def __init__(self):
            self.EndPositionXYZScale = []
            self.StartPositionXYZScale = []
            self.Rotation = []
            self.BoneNameOffset = 0
            self.unk0 = []
            self.unk1 = 0
            self.BoneParentIdx = 0
            self.BoneIdx = 0
            self.unk2 = 0
            self.Name = ""
        def read(self,f):
            self.EndPositionXYZScale = f.f32_4()
            self.StartPositionXYZScale = f.f32_4()
            self.Rotation = f.f32_3()
            self.BoneNameOffset = f.u32()
            self.unk0 = f.f32_3()
            self.unk1 = f.u8()
            self.BoneParentIdx = f.u8()
            self.BoneIdx = f.u8()
            self.unk2 = f.u8()
            if(self.BoneNameOffset):
                self.Name = f.getString(self.BoneNameOffset)
    class WeightTable(object):
        class WeightDef(object):
            def __init__(self):
                self.Pos = [0.0]*3
                self.bWgt = 1.0
                self.Nor = [0.0]*3
                self.bIdx = 0
                self.stat = 0
            def read(self,f):
                self.Pos = f.f32_3()
                self.bWgt = f.f32()
                self.Nor = f.f32_3()
                self.bIdx = f.u8()
                self.stat = f.u8()
                if(self.stat):
                    print(self.stat)
                f.seek(2,1)
        def __init__(self):
            self.VertCounts = [0]*4
            self.WeightBufferOffset = 0
            self.VertBuffer1Offset = 0
            self.VertBuffer2Offset = 0
            self.WeightBuffer1 = []
            self.WeightBuffer2 = []
            self.WeightBuffer3 = []
            self.WeightBuffer4 = []
        def read(self,f):
            for x in range(4):
                self.VertCounts[x] = f.u32()
            self.WeightBufferOffset = f.u32()
            self.VertBuffer1Offset = f.u32()
            self.VertBuffer2Offset = f.u32()
            for idx,x in enumerate(self.VertCounts):
                if(idx == 0):
                    self.WeightBuffer1 = [self.WeightDef()] * x
                elif(idx == 1):
                    self.WeightBuffer2 = [self.WeightDef()] * (x * 2)
                elif(idx == 2):
                    self.WeightBuffer3 = [self.WeightDef()] * (x * 3)
            f.seek(self.WeightBufferOffset)
            for x in range(len(self.WeightBuffer1)):
                a = self.WeightDef()
                a.read(f)
                self.WeightBuffer1[x] = a
            for x in range(len(self.WeightBuffer2)):
                a = self.WeightDef()
                a.read(f)
                self.WeightBuffer2[x] = a
            for x in range(len(self.WeightBuffer3)):
                a = self.WeightDef()
                a.read(f)
                self.WeightBuffer3[x] = a
            high = 4
            for x in range(self.VertCounts[3]):
                arr = []
                for y in range(high):
                    a = self.WeightDef()
                    a.read(f)
                    arr.append(a)
                    if(a.stat == 1):
                        high +=1
                self.WeightBuffer4.append(arr)
    def __init__(self):
        self.f = None
        self.header = self.Header()
        self.unkMtx = self.MatrixUnk()
        self.wgtTbl = self.WeightTable()
        self.matrix_table = []
        self.boneInfo = []
    def read(self,f):
        self.f = FRead(f)
        self.header.read(self.f)
        self.f.seek(self.header.ukn_MatrixTableOffset)
        self.unkMtx.read(self.f)
        self.f.seek(self.header.MatricesInfo[1])
        skipAmount = 320
        if(self.header.Endian):
            skipAmount = 256
        for x in range(self.header.MatricesInfo[0]):
            a = self.MatrixTable()
            a.read(self.f)
            self.matrix_table.append(a)
            self.f.seek(skipAmount,1)
        self.f.seek(self.header.BoneInfo[1])
        for x in range(self.header.BoneInfo[0]):
            a = self.BoneInfo()
            a.read(self.f)
            self.boneInfo.append(a)
        self.f.seek(self.header.WeightTableOffset)
        self.wgtTbl.read(self.f)
