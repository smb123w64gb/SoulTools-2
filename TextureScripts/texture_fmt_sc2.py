import struct
from enum import Enum
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

def u8(file):
    return struct.unpack("B", file.read(1))[0]
 
def u16be(file):
    return struct.unpack(">H", file.read(2))[0]
 
def u16le(file):
    return struct.unpack("<H", file.read(2))[0]

def u32be(file):
    return struct.unpack(">I", file.read(4))[0]
 
def u32le(file):
    return struct.unpack("<I", file.read(4))[0]
 
def f32be(file):
    return struct.unpack(">f", file.read(4))[0]
 
def f32le(file):
    return struct.unpack("<f", file.read(4))[0]


def w32(file,val):
    file.write(struct.pack("<I", val))
def w16(file,val):
    file.write(struct.pack("<H", val))
def w8(file,val):
    file.write(struct.pack("B", val))

def calcSize(w,h,fmt):
    if(fmt == D3DFORMAT.D3DFMT_DXT1):
        return (w*h)/2
    else:
        return (w*h)

class VTX(object):
    class Header(object):
        def __init__(self):
            self.Magic = b'VXT.'
            self.type = 2
            self.flag0 = 4
            self.flag1 = 2
            self.flag2 = 0
            self.textureCount = 0
            self.headerlen = 20
            self.HeaderBlockSize = 0
        def read(self,f):
            self.Magic = f.read(4)
            self.type = u8(f)
            self.flag0 = u8(f)
            self.flag1 = u8(f)
            self.flag2 = u8(f)
            self.textureCount = u32le(f)
            self.headerlen = u32le(f)
            self.HeaderBlockSize = u32le(f)
        def write(self,f):
            f.write(self.Magic)
            w8(f,self.type)
            w8(f,self.flag0)
            w8(f,self.flag1)
            w8(f,self.flag2)
            w32(f,self.textureCount)
            w32(f,self.headerlen)
            w32(f,self.HeaderBlockSize)
    class Texture(object):
        class Pallet(object):
            def __init__(self):
                self.PaletteOffset = 0
                self.PaletteCount = 256 #Max anyways
                self.Padd = 0
                self.Data = [0xFF000000]*256
            def read(self,f):
                self.PaletteOffset = u32le(f)
                self.PaletteCount = u32le(f)
                self.Padd = u32le(f)
                ret = f.tell()
                f.seek(self.PaletteOffset)
                self.Data = []
                for x in range(self.PaletteCount):
                    self.Data.append(u32le(f))
                f.seek(ret)
            def writeEnt(self,f):
                w32(f,self.PaletteOffset)
                w32(f,self.PaletteCount)
                w32(f,self.Padd)
            def writeData(self,f):
                for x in self.Data:
                    w32(f,x)
                for x in range(len(self.Data) - 256):
                    w32(f,x)
        def __init__(self):
            self.pallet = None
            self.palletOff = 0
            self.flags = 9243 #need real flags later
            self.Unk1 = 0
            self.HeightVisible = 0
            self.WidthVisible = 0
            self.DataOffset = 0
            self.ImageType = D3DFORMAT.D3DFMT_DXT1
            self.Height = 0
            self.Width = 0
            self.MipMapCount = 1
            self.Pad2 = 0
            self.Data = []
        def read(self,f):
            self.palletOff = u32le(f)
            if(self.palletOff>0):
                ret = f.tell()
                f.seek(self.palletOff)
                self.pallet = self.Pallet()
                self.pallet.read(f)
                f.seek(ret)
            self.flags = u32le(f)
            self.Unk1 = u32le(f)
            self.HeightVisible = u16le(f)
            self.WidthVisible = u16le(f)
            self.DataOffset = u32le(f)
            self.ImageType = D3DFORMAT(u32le(f))
            self.Height = u16le(f)
            self.Width = u16le(f)
            self.MipMapCount = u32le(f)
            self.Pad2 = u32le(f)
            sizeOfData = 0
            w = 0
            h = 0
            for x in range(self.MipMapCount):
                if(x == 0):
                    w = self.Width
                    h = self.Height
                else:
                    w >>= 1
                    h >>= 1
                sizeOfData += calcSize(w,h,self.ImageType)
            ret = f.tell()
            f.seek(self.DataOffset)
            self.Data = f.read(sizeOfData)
            f.seek(ret)
        def write(self,f):
            w32(f,self.palletOff)
            w32(f,self.flags)
            w32(f,self.Unk1)
            w16(f,self.HeightVisible)
            w16(f,self.WidthVisible)
            w32(f,self.DataOffset)
            w32(f,self.ImageType.value)
            w16(f,self.Height)
            w16(f,self.Width)
            w32(f,self.MipMapCount)
            w32(f,self.Pad2)
    def __init__(self):
        self.header = self.Header()
        self.textures = []
    def read(self,f):
        self.header.read(f)
        for x in range(self.header.textureCount):
            tex = self.Texture()
            tex.read(f)
            self.textures.append(tex)
    def recalc(self):
        self.header.HeaderBlockSize = (len(self.textures) * 0x24)+0x14
        self.header.textureCount = len(self.textures)
        Head = (len(self.textures) * 0x24)+0x14
        #First pass is for Pallet Entrys(If they exist)
        for x in self.textures:
            if x.pallet is not None:
                x.palletOff = Head
                Head += 12
        if(Head % 0x40):#Also alignment
            Head += 0x40 - (Head % 0x40)
        #Second pass, Pallete Data asume all of em are 256 * 4 (1024)
        for x in self.textures:
            if x.pallet is not None:
                x.pallet.PaletteOffset = Head
                Head += 0x400
        if(Head % 0x100):#Also alignment
            Head += 0x100 - (Head % 0x100)
        #Third, Now for Texel Data
        for x in self.textures:
            x.DataOffset = Head
            Head += len(x.Data)
    def write(self,f):
        self.recalc() #Good idea so we know everything is squared up
        self.header.write(f)
        for x in self.textures:
            x.write(f)
        for x in self.textures:
            if x.pallet is not None:
                x.pallet.writeEnt(f)
        misAlignment =  f.tell() % 0x40
        if(misAlignment):
            for x in range(0x40 - misAlignment):
                w8(f,0)#Seeking wont write null so we do it
        for x in self.textures:
            if x.pallet is not None:
                x.pallet.writeData(f)
        misAlignment =  f.tell() % 0x100
        if(misAlignment):
            for x in range(0x100 - misAlignment):
                w8(f,0)#Seeking wont write null so we do it
        for x in self.textures:
            f.write(x.Data)
    def addTexture(self,w,h,data,mipCount,format,pallet = None):
        newTex = self.Texture()
        newTex.Width = w
        newTex.WidthVisible = w
        newTex.Height = h
        newTex.HeightVisible = h
        newTex.MipMapCount = mipCount
        newTex.Data = data
        newTex.ImageType = format
        if pallet is not None:
            newPal = self.Texture().Pallet()
            newPal.Data = pallet
            newTex.pallet = newPal
        self.textures.append(newTex)