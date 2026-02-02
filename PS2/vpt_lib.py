import struct
from ctypes import *
from enum import auto, Enum

def u8(file):
    return struct.unpack("B", file.read(1))[0]
 
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
 
def u32(file):
    return struct.unpack("<I", file.read(4))[0]

def u64(file):
    return struct.unpack("<Q", file.read(8))[0]
 
def f32(file):
    return struct.unpack("<f", file.read(4))[0]

def w64(file,val):
    file.write(struct.pack("<Q", val))

def w32(file,val):
    file.write(struct.pack("<I", val))

def w16(file,val):
    file.write(struct.pack("<H", val))

def w8(file,val):
    file.write(struct.pack("B", val))
def read_return(file,offset,size):
    ret = file.tell()
    file.seek(offset)
    data = file.read(size)
    file.seek(ret)
    return data
class GS_Gif_Tag(Structure):
    _pack_ = 1
    _fields_ = [
            ("nloop", c_uint64, 15),
            ("eop", c_uint64, 1),
            ("pad1", c_uint64, 30),
            ("pre", c_uint64, 1),
            ("prim", c_uint64, 11),
            ("flg", c_uint64, 2),
            ("nreg", c_uint64, 4),
            ("reg", c_uint64, 64),
        ]
class Dma_Tag_bits(Structure):
    _fields_ = [
            ("QWC", c_uint, 16),
            ("PAD", c_uint, 10),
            ("PCE", c_uint, 2),
            ("ID", c_uint, 3),
            ("IRQ", c_uint, 1),
            ("ADDR", c_uint, 31),
            ("SPR", c_uint, 1),
        ]
class DMA_Tag_Type(Enum):
    P2_DMA_TAG_REFE = 0
    P2_DMA_TAG_CNT = 1
    P2_DMA_TAG_NEXT = 2
    P2_DMA_TAG_REF = 3
    P2_DMA_TAG_REFS = 4
    P2_DMA_TAG_CALL = 5
    P2_DMA_TAG_RET = 6
    P2_DMA_TAG_END = 7
class GS_REG(Enum):
    PRIM        = 0x00  # Select and configure current drawing primitive
    RGBAQ       = 0x01  # Setup current vertex color
    ST          = 0x02  # ST map
    UV          = 0x03  # UV map
    XYZF2       = 0x04  # Set vertex position and fog coefflcient (with draw kick)
    XYZ2        = 0x05  # Set vertex coordinate (with draw kick)
    TEX0_1      = 0x06  # Select current texture in context 1
    TEX0_2      = 0x07  # Select current texture in context 2
    CLAMP_1     = 0x08  # Set texture wrap mode in context 1
    CLAMP_2     = 0x09  # Set texture wrap mode in context 2
    FOG         = 0x0a  # Set fog attributes
    XYZF3       = 0x0c  # Set vertex position and fog coefflcient (no draw kick)
    XYZ3        = 0x0d  # Set vertex position (no draw kick)
    AD_NOREG          = 0x0e  # A+D
    NOP_NOREG         = 0x0f  # NOP (Not OutPut)
    TEX1_1      = 0x14
    TEX1_2      = 0x15
    TEX2_1      = 0x16  # Set texture filtering\sampling style in context 1
    TEX2_2      = 0x17  # Set texture filtering\sampling style in context 2
    XYOFFSET_1  = 0x18  # Mapping from Primitive to Window coordinate system (Context 1)
    XYOFFSET_2  = 0x19  # Mapping from Primitive to Window coordinate system (Context 2)
    PRMODECONT  = 0x1a  # gs_g_prim or gs_g_prmode selector
    PRMODE      = 0x1b  # attributes of current drawing primitive
    TEXCLUT     = 0x1c
    SCANMSK     = 0x22  # Raster odd\even line drawing setting
    MIPTBP1_1   = 0x34  # Set mipmap address in context 1(mip level 1-3)
    MIPTBP1_2   = 0x35  # Set mipmap address in context 1(mip level 1-3)
    MIPTBP2_1   = 0x36  # Set mipmap address in context 2(mip level 4-6)
    MIPTBP2_2   = 0x37  # Set mipmap address in context 2(mip level 4-6)
    TEXA        = 0x3b  # Texture alpha setting
    FOGCOL      = 0x3d  # Set fog far color
    TEXFLUSH    = 0x3f  # Flush texture buffer/cache
    SCISSOR_1   = 0x40  # Setup clipping rectangle (Context 1)
    SCISSOR_2   = 0x41  # Setup clipping rectangle (Context 2)
    ALPHA_1     = 0x42  # Alpha blending setting (Context 1)
    ALPHA_2     = 0x43  # Alpha blending setting (Context 2)
    DIMX        = 0x44  # Dither matrix values
    DTHE        = 0x45  # Enabel dither matrix
    COLCLAMP    = 0x46  # Color clamp control
    TEST_1      = 0x47  # FrameBuffer\ZBuffer Pixel test contol (Context 1)
    TEST_2      = 0x48  # FrameBuffer\ZBuffer Pixel test contol (Context 2)
    PABE        = 0x49  # Enable alpha blending
    FBA_1       = 0x4a  # Alpha correction value (Context 1)
    FBA_2       = 0x4b  # Alpha correction value (Context 2)
    FRAME_1     = 0x4c  # Frame buffer settings (Context 1)
    FRAME_2     = 0x4d  # Frame buffer settings (Context 2)
    ZBUF_1      = 0x4e  # Zbuffer configuration (Context 1)
    ZBUF_2      = 0x4f  # Zbuffer configuration (Context 2)
    BITBLTBUF   = 0x50  # Texture transmission address & format
    TRXPOS      = 0x51  # Texture transmission coordinates
    TRXREG      = 0x52  # Texture transmission width & height
    TRXDIR      = 0x53  # Texture transmission direction
    HWREG       = 0x54
    SIGNAL      = 0x60
    FINISH      = 0x61
    LABEL       = 0x62
    NOP         = 0x7f  # no operation\does nothing\can be used as padding

class Gif_Tag(object):
    def __init__(self):
        self.bits:GS_Gif_Tag = GS_Gif_Tag()
    def read(self,f):
        self.bits = GS_Gif_Tag.from_buffer_copy(f.read(16))
    def readbuf(self,f):
        self.bits = GS_Gif_Tag.from_buffer_copy(f[:16])
    def __str__(self):
        sring = ''
        sring += GS_REG(self.bits.reg).name
        return sring
    def write(self,f):
        f.write(bytes(self.bits))

class Dma_Tag(object):
    def __init__(self):
        self.bits: Dma_Tag_bits = Dma_Tag_bits()
        self.OPT1 = 0
        self.OPT2 = 0
        self.next : Dma_Tag = None
        self.data = None
    def read(self,f):
        self.bits = Dma_Tag_bits.from_buffer_copy(f.read(8))
        self.OPT1 = u32(f)
        self.OPT2 = u32(f)
        ret = f.tell()
        if(DMA_Tag_Type(self.bits.ID) == DMA_Tag_Type.P2_DMA_TAG_CALL):
            f.seek(self.bits.ADDR)
            tag = Dma_Tag()
            tag.read(f)
            self.next = tag
        elif(DMA_Tag_Type(self.bits.ID) == DMA_Tag_Type.P2_DMA_TAG_CNT):
            self.data = f.read(self.bits.QWC*16)
            tag = Dma_Tag()
            tag.read(f)
            self.next = tag
        elif(DMA_Tag_Type(self.bits.ID) == DMA_Tag_Type.P2_DMA_TAG_REF):
            self.data = read_return(f,self.bits.ADDR,self.bits.QWC*16)
            tag = Dma_Tag()
            tag.read(f)
            self.next = tag
        f.seek(ret)
        

    def write(self,f):
        w64(f,self.bits.asbyte)
        w32(f,self.OPT1)
        w32(f,self.OPT2)
    def __str__(self):
        sring = ''
        sring += str("%s,Offset:@ %s Transfer %s"%(DMA_Tag_Type(self.bits.ID).name,hex(self.bits.ADDR),hex(self.bits.QWC*16)))
        return sring
isThree = False
class VTP(object):
    def __init__(self):
        self.header = self.Header()
        self.dma_ents = []
    def read(self,f):
        self.header.read(f)
        f.seek(self.header.dmaTableHeader)
        for x in range(self.header.dmaCount):
            entrys = self.DMATable()
            entrys.read(f)
            self.dma_ents.append(entrys)
    class Header(object):
        def __init__(self):
            self.Magic = 2
            self.offset2DMAs = 4
            self.offsetCount = 4
            self.dmaCount = 1
            self.textureCount = 1
            self.dmaTableHeader = 0
            self.textureTableHeader = 0
            self.creditsOne = 0
            self.creditsTwo = 0
            self.extendOffsetOne = 0
            self.extendOffsetTwo = 0
        def __str__(self):
            stringout = ''
            stringout+= str('VTP Ver %i\n' % self.Magic)
            stringout+=str('Offset Count %i\n' % self.offsetCount)
            stringout+=str('DMA offset @ %i\n' % self.offset2DMAs)
            stringout+=str('DMA Chain Count %i\n' % self.dmaCount)

            stringout+=str('\nTexture Count %i\n' % self.textureCount)
            return stringout

        def read(self,f):
            self.Magic = u8(f)
            if(self.Magic == 3):
                global isThree
                isThree = True
            self.offset2DMAs = u8(f)
            self.offsetCount = u8(f)
            u8(f)
            self.dmaCount = u8(f)
            self.textureCount = u8(f)
            u16(f)
            self.dmaTableHeader = u32(f)
            self.textureTableHeader = u32(f)
            self.creditsOne = u32(f)
            self.creditsTwo = u32(f)
            self.extendOffsetOne = u32(f)
            self.extendOffsetTwo = u32(f)
        def write(self,f):
            w8(f,self.Magic)
            w8(f,self.offset2DMAs)
            w8(f,self.offsetCount)
            w8(f,0)

            w8(f,self.dmaCount)
            w8(f,self.textureCount)
            w16(f,0)
            w32(f,self.dmaTableHeader)
            w32(f,self.textureTableHeader)
            w32(f,self.creditsOne)
            w32(f,self.creditsTwo)
            w32(f,self.extendOffsetOne)
            w32(f,self.extendOffsetTwo)
    class UploadInfo(object):
        def __init__(self):
            headTag = Dma_Tag()
            
    class DMATable(object):
        class DMATableHeader(object):
            def __init__(self):
                self.offset = 0x20
                self.count = 0
                self.magic = 0x2C40
                self.unk = 0 #SC3 Specal
            def read(self,f):
                self.offset = u64(f)
                self.count = u16(f)
                self.magic = u16(f)
                global isThree
                if(isThree):
                   self.unk = u64(f) 
            def write(self,f):
                w64(self.offset)
                w16(self.count)
                w16(self.magic)
                global isThree
                if(isThree):
                    w64(self.unk)
        def __init__(self):
            self.TableHeader = self.DMATableHeader()
            self.DMAChains = []
        def read(self,f):
            self.TableHeader.read(f)
            ret = f.tell()
            f.seek(self.TableHeader.offset)
            for x in range(self.TableHeader.count):
                tag = Dma_Tag()
                tag.read(f)
                self.DMAChains.append(tag)
            #end Tag why not
            tag = Dma_Tag()
            tag.read(f)
            self.DMAChains.append(tag)
            f.seek(ret)
