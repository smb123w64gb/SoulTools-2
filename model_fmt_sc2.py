import struct
from enum import Flag, auto, Enum
class D3DFORMAT(Enum):
    D3DFMT_L8 = 0x00
    D3DFMT_AL8 = 0x01
    D3DFMT_A1R5G5B5 = 0x02
    D3DFMT_X1R5G5B5 = 0x03
    D3DFMT_A4R4G4B4 = 0x04
    D3DFMT_R5G6B5 = 0x05
    D3DFMT_A8R8G8B8 = 0x06
    D3DFMT_X8R8G8B8 = 0x07
    D3DFMT_X8L8V8U8 = 0x07 # Alias

    D3DFMT_P8 = 0x0b # 8-bit Palletized

    D3DFMT_A8 = 0x19
    D3DFMT_A8L8 = 0x1a
    D3DFMT_R6G5B5 = 0x27
    D3DFMT_L6V5U5 = 0x27 # Alias

    D3DFMT_G8B8 = 0x28
    D3DFMT_V8U8 = 0x28 # Alias

    D3DFMT_R8B8 = 0x29
    D3DFMT_D24S8 = 0x2a
    D3DFMT_F24S8 = 0x2b
    D3DFMT_D16 = 0x2c
    D3DFMT_D16_LOCKABLE = 0x2c # Alias

    D3DFMT_F16 = 0x2d
    D3DFMT_L16 = 0x32
    D3DFMT_V16U16 = 0x33
    D3DFMT_R5G5B5A1 = 0x38
    D3DFMT_R4G4B4A4 = 0x39
    D3DFMT_A8B8G8R8 = 0x3A
    D3DFMT_Q8W8V8U8 = 0x3A # Alias

    D3DFMT_B8G8R8A8 = 0x3B
    D3DFMT_R8G8B8A8 = 0x3C

    # YUV Formats

    D3DFMT_YUY2 = 0x24
    D3DFMT_UYVY = 0x25

    # Compressed Formats

    D3DFMT_DXT1 = 0x0C # opaque/one-bit alpha
    D3DFMT_DXT2 = 0x0E # Alias for D3DFMT_DXT3
    D3DFMT_DXT3 = 0x0E # linear alpha
    D3DFMT_DXT4 = 0x0F # Alias for D3DFMT_DXT5
    D3DFMT_DXT5 = 0x0F # interpolated alpha

    # Linear Formats

    D3DFMT_LIN_A1R5G5B5 = 0x10
    D3DFMT_LIN_R5G6B5 = 0x11
    D3DFMT_LIN_A8R8G8B8 = 0x12
    D3DFMT_LIN_L8 = 0x13
    D3DFMT_LIN_R8B8 = 0x16
    D3DFMT_LIN_G8B8 = 0x17
    D3DFMT_LIN_V8U8 = 0x17 # Alias

    D3DFMT_LIN_AL8 = 0x1b
    D3DFMT_LIN_X1R5G5B5 = 0x1c
    D3DFMT_LIN_A4R4G4B4 = 0x1d
    D3DFMT_LIN_X8R8G8B8 = 0x1e
    D3DFMT_LIN_X8L8V8U8 = 0x1e # Alias

    D3DFMT_LIN_A8 = 0x1f
    D3DFMT_LIN_A8L8 = 0x20
    D3DFMT_LIN_D24S8 = 0x2E
    D3DFMT_LIN_F24S8 = 0x2f
    D3DFMT_LIN_D16 = 0x30
    D3DFMT_LIN_F16 = 0x31
    D3DFMT_LIN_L16 = 0x35
    D3DFMT_LIN_V16U16 = 0x36
    D3DFMT_LIN_R6G5B5 = 0x37
    D3DFMT_LIN_L6V5U5 = 0x37 # Alias

    D3DFMT_LIN_R5G5B5A1 = 0x3D
    D3DFMT_LIN_R4G4B4A4 = 0x3e
    D3DFMT_LIN_A8B8G8R8 = 0x3f
    D3DFMT_LIN_B8G8R8A8 = 0x40
    D3DFMT_LIN_R8G8B8A8 = 0x41
class FmtTXVFlag(Flag):
    BIT01 = auto()
    CLAMP = auto()
    BIT03 = auto()
    BIT04 = auto()
    TWOSIDED = auto()
    BIT06 = auto()
    BIT07 = auto()
    BIT08 = auto()
    SPEC  = auto()
    BIT10 = auto()
    BIT11 = auto()
    BIT12 = auto()
    BIT13 = auto()
    BIT14 = auto()
    BIT15 = auto()
    BIT16 = auto()
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
    def u8_4(self):
        return struct.unpack(self.endian+'BBBB', self.file.read(4))[0:4]
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
    def f32_2(self):
        return struct.unpack(self.endian+'ff', self.file.read(8))[0:2]
    def seek(self,offset,whence=0):
        self.file.seek(offset,whence)
    def tell(self):
        return self.file.tell()
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
        def __str__(self):
            rt = ""
            rt += str("Magic: %s\n" % self.MAGIC)
            rt += str("Ver: %i\n" % self.Version)
            rt += str("ModelContent: %i\n"%self.ModelContent)
            rt += str("Matrix count %i @ %s\n"%(self.MatricesInfo[0],hex(self.MatricesInfo[1])))
            rt += str("Layer0Info count %i @ %s\n"%(self.Layer0Info[0],hex(self.Layer0Info[1])))
            rt += str("Layer1Info count %i @ %s\n"%(self.Layer1Info[0],hex(self.Layer1Info[1])))
            rt += str("Layer2Info count %i @ %s\n"%(self.Layer2Info[0],hex(self.Layer2Info[1])))
            rt += str("BoneInfo count %i @ %s\n"%(self.BoneInfo[0],hex(self.BoneInfo[1])))
            rt += str("MaterialsInfo count %i @ %s\n"%(self.MaterialsInfo[0],hex(self.MaterialsInfo[1])))
            return rt
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
    class Texture(object):
        class Data(object):
            def __init__(self):
                self.TexturePaletteCLUTOffset = 0 #TEXTURE PALETTE ROW OFFSET
                self.Flags = 0
                self.Unk1 = 0 #00000000
                self.HeightVisible = 0 #visible height ONLY IN TYPE 2
                self.WidthVisible = 0 #visible width ONLY IN TYPE 2
                self.TextureDataOffset = 0 # color look up table, if DXT this is the image data addr
                self.ImageType = D3DFORMAT.D3DFMT_DXT1 #DirectX spec texture enum
                self.Height = 0 # dimension but in multiples of 8
                self.Width = 0 # dimension but in multiples of 8
                self.MipMapCount = 1 # mip count range [1 - 6]
                self.Pad2 = 0 # pad to align
                self.DiffuseBytes = bytearray.fromhex("1BF8000005055050")
                self.MipMapBytes = bytearray()
                self.Palette = bytearray()
                self.TextureSize = 0
        def __init__(self):
            self.MAGIC = "VXT"
            self.type = 0
            self.Unk01_flag = 0
            self.Unk02_flag = 0
            self.Pad = 0
            self.TextureCount = 0
            self.Pad2 = 0
            self.HeaderLength = 0
            self.HeaderBlockSize = 0
        def read(self,f):
            self.MAGIC = f.read(4)
            self.type = f.u8()
            self.Unk01_flag = f.u8()
            self.Unk02_flag = f.u8()
            self.Pad = f.u8()
            self.TextureCount = f.u32()
            self.HeaderLength = f.u32()
            self.HeaderBlockSize = f.u32()
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
                f.seek(2,1)
            def as_bytes(self):
                return struct.pack('fffffffBBH',self.Pos[0],self.Pos[1],self.Pos[2],self.bWgt,self.Nor[0],self.Nor[1],self.Nor[2],self.bIdx,self.stat,0)
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
    
    class LayerObjectEntryXbox(object):
        class BufferColorUV(object):
            def __init__(self):
                self.RGBA = [255]*4
                self.UV = [0.0]*2
            def read(self,f):
                self.RGBA = f.u8_4()
                self.UV = f.f32_2()
        class BufferScaleVertex(object):
            def __init__(self):
                self.Position = [0.0] * 3
                self.PositionScale = 1.0
                self.Normal = [0.0] * 3
                self.NormalScale = 1.0
            def read(self,f):
                self.Position = f.f32_3()
                self.PositionScale = f.f32()
                self.Normal = f.f32_3()
                self.NormalScale = f.f32()
        class BufferStaticVertex(object):
            def __init__(self):
                self.Position = [0.0] * 3
                self.Normal = [0.0] * 3
                self.RGBA = [255]*4
                self.UV = [0.0]*2
                self.pad = 0
            def read(self,f):
                self.Position = f.f32_3()
                self.Normal = f.f32_3()
                self.RGBA = f.u8_4()
                self.UV = f.f32_2()
                self.pad = f.u32()
        def __init__(self):
            self.ObjectType = 0
            self.PrimitiveType = 0
            self.FaceCount = 0
            self.MatrixOffset = 0
            self.MaterialOffset = 0
            self.FaceOffset = 0
            self.Buffer1Offset = 0
            self.Buffer2Offset = 0
            self.Buffer3Offset = 0
            self.Buffer4Offset = 0
            self.CenterRadiusOffset = 0
            self.Mesh = []
            self.RiggedVerts = [[]] * 3 #UV + Scalable Poss + UNK?
            self.StaticVerts = [] 
        def findmaxVerts(self):
            maxi = 0
            for x in self.Mesh:
                
                if(x == 0xFFFF):
                    pass
                elif(maxi < x):
                    maxi = x
            return maxi
        def read(self,f):
                self.ObjectType = f.u16()
                self.PrimitiveType = f.u16()
                self.FaceCount = f.u32()
                self.MatrixOffset = f.u32()
                self.MaterialOffset = f.u32()
                self.FaceOffset = f.u32()
                self.Buffer1Offset = f.u32()
                self.Buffer2Offset = f.u32()
                self.Buffer3Offset = f.u32()
                self.Buffer4Offset = f.u32()
                self.CenterRadiusOffset = f.u32()
                fret = f.tell()
                f.seek(self.FaceOffset)
                for x in range(self.FaceCount):
                    self.Mesh.append(f.u16())
                vertCount = self.findmaxVerts()
                if(self.ObjectType == 4):
                    f.seek(self.Buffer1Offset)
                    uvs = []
                    for x in range(vertCount):
                        uv = self.BufferColorUV()
                        uv.read(f)
                        uvs.append(uv)
                    self.RiggedVerts[0] = uvs
                    f.seek(self.Buffer2Offset)
                    verts = []
                    for x in range(vertCount):
                        vert = self.BufferScaleVertex()
                        vert.read(f)
                        verts.append(vert)
                    self.RiggedVerts[1] = verts
                    f.seek(self.Buffer3Offset)
                    verts = []
                    for x in range(vertCount):
                        vert = self.BufferScaleVertex()
                        vert.read(f)
                        verts.append(vert)
                    self.RiggedVerts[2] = verts
                    
                else:
                    f.seek(self.Buffer4Offset)
                    for x in range(vertCount):
                        vert = self.BufferStaticVertex()
                        vert.read(f)
                        self.StaticVerts.append(vert)
                f.seek(fret)
                    
        def __str__(self):
            rt = ""

            if(self.ObjectType == 0):
                rt += "STATIC\n"
            elif(self.ObjectType == 4):
                rt += "SKINNED\n"
            else:
                rt += str("UNK %i\n" % self.ObjectType)

            if(self.PrimitiveType == 0):
                rt += "TRIANGLESTRIP\n"
            elif(self.PrimitiveType == 1):
                rt += "TRIANGLELIST\n"
            else:
                rt += str("UNK %i\n" % self.PrimitiveType)
            rt += str("Face Count: %i @ %s\n" % (self.FaceCount,hex(self.FaceOffset)))
            return rt
            
    def __init__(self):
        self.f = None
        self.header = self.Header()
        self.unkMtx = self.MatrixUnk()
        self.wgtTbl = self.WeightTable()
        self.matrix_table = []
        self.boneInfo = []
        self.Object_0 = []
        self.Object_1 = []
        self.Object_2 = []
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
        self.f.seek(self.header.Layer0Info[1])
        for x in range(self.header.Layer0Info[0]):
            Layer = self.LayerObjectEntryXbox()
            Layer.read(self.f)
            self.Object_0.append(Layer)
        self.f.seek(self.header.Layer1Info[1])
        for x in range(self.header.Layer1Info[0]):
            Layer = self.LayerObjectEntryXbox()
            Layer.read(self.f)
            self.Object_1.append(Layer)
        self.f.seek(self.header.Layer2Info[1])
        for x in range(self.header.Layer2Info[0]):
            Layer = self.LayerObjectEntryXbox()
            Layer.read(self.f)
            self.Object_2.append(Layer)
