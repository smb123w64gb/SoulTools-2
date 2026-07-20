import struct
from ctypes import *

class TexMode0(Structure):
    _pack_ = 1
    _fields_ = [
            ("wrap_s", c_uint32, 2),
            ("wrap_t", c_uint32, 2),
            ("mag_filter", c_uint32, 1),
            ("mipmap_filter", c_uint32, 2),
            ("min_filter", c_uint32, 1),
            ("diag_lod", c_uint32, 1),
            ("lod_bias", c_uint32, 8),
            ("max_aniso", c_uint32, 2),
            ("lod_clamp", c_uint32, 1),
        ]
class TexImage0(Structure):
    _pack_ = 1
    _fields_ = [
            ("width", c_uint32, 10),
            ("height", c_uint32, 10),
            ("format", c_uint32, 4),
            ("pad", c_uint32, 8),
        ]
class TexTLUT(Structure):
    _pack_ = 1
    _fields_ = [
            ("tmem_offset", c_uint32, 10),
            ("tlut_format", c_uint32, 2),
            ("pad", c_uint32, 20),
        ]


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
    file.write(struct.pack(">I", val))
def w16(file,val):
    file.write(struct.pack(">H", val))
def w8(file,val):
    file.write(struct.pack("B", val))

def calcSize(w,h,fmt):
    if(fmt == D3DFORMAT.D3DFMT_DXT1):
        return (w*h)/2
    else:
        return (w*h)

class VTG(object):
    class Header(object):
        def __init__(self):
            self.Magic = b'VGT.'
            self.type = 4
            self.flag0 = 0
            self.flag1 = 0
            self.flag2 = 0
            self.textureCount = 0
            self.unk0 = 0
            self.headerlen = 24
            self.HeaderBlockSize = 0
        def read(self,f):
            self.Magic = f.read(4)
            self.type = u8(f)
            self.flag0 = u8(f)
            self.flag1 = u8(f)
            self.flag2 = u8(f)
            self.textureCount = u32be(f)
            self.unk0 = u32be(f)
            self.headerlen = u32be(f)
            self.HeaderBlockSize = u32be(f)
        def write(self,f):
            f.write(self.Magic)
            w8(f,self.type)
            w8(f,self.flag0)
            w8(f,self.flag1)
            w8(f,self.flag2)
            w32(f,self.textureCount)
            w32(f,self.unk0)
            w32(f,self.headerlen)
            w32(f,self.HeaderBlockSize)
    class Texture(object):
        class Pallet(object):
            def __init__(self):
                self.Reserved = 0
                self.PaletteOffset = 0
                self.TexTlut = TexTLUT()
                self.Data = [0xFFFF]*256
            def read(self,f):
                self.Reserved = u32be(f)
                self.PaletteOffset = u32be(f)
                self.TexTlut= TexTLUT.from_buffer_copy(u32be(f))
            def writeEnt(self,f):
                w32(f,self.Reserved)
                w32(f,self.PaletteOffset)
                f.write(bytes(self.TexTlut))#GC is tad diff with getting pallet count via CI# so get data later
        def __init__(self):
            self.pallet = None
            self.palletOff = 0
            self.flags = 9225 #need real flags later
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
            self.palletOff = u32be(f)
            if(self.palletOff>0):
                ret = f.tell()
                f.seek(self.palletOff)
                self.pallet = self.Pallet()
                self.pallet.read(f)
                f.seek(ret)
            self.flags = u32be(f)
            self.Unk1 = u32be(f)
            self.HeightVisible = u16le(f)
            self.WidthVisible = u16le(f)
            self.DataOffset = u32be(f)
            self.ImageType = D3DFORMAT(u32be(f))
            self.Height = u16le(f)
            self.Width = u16le(f)
            self.MipMapCount = u32be(f)
            self.Pad2 = u32be(f)
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
            if(Head % 0x100):#Also alignment
                Head += 0x100 - (Head % 0x100)
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
            misAlignment =  f.tell() % 0x100
            if(misAlignment):
                for x in range(0x100 - misAlignment):
                    w8(f,0)#Seeking wont write null so we do it
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