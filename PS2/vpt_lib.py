import struct
from ctypes import *

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




class Dma_Tag(object):
    tag_names = ["P2_DMA_TAG_REFE","P2_DMA_TAG_CNT","P2_DMA_TAG_NEXT","P2_DMA_TAG_REF","P2_DMA_TAG_REFS","P2_DMA_TAG_CALL","P2_DMA_TAG_RET","P2_DMA_TAG_END"]
    class Dma_Tag_Header(Union):
        class Dma_Tag_bits(LittleEndianStructure):
                _fields_ = [
                        ("QWC", c_uint16, 16),
                        ("PAD", c_uint16, 10),
                        ("PCE", c_uint8, 2),
                        ("ID", c_uint8, 3),
                        ("IRQ", c_uint8, 1),
                        ("ADDR", c_uint32, 31),
                        ("SPR", c_uint8, 1),
                    ]
        _fields_ = [("b", Dma_Tag_bits),
                    ("asbyte", c_uint64)]
    def __init__(self):
        self.bits = self.Dma_Tag_Header()
        self.bits.asbyte = 0
        self.OPT1 = 0
        self.OPT2 = 0
    def read(self,f):
        self.bits.asbyte = u64(f)
        self.OPT1 = u32()
        self.OPT2 = u32()
    def write(self,f):
        w64(f,self.bits.asbyte)
        w32(f,self.OPT1)
        w32(f,self.OPT2)
    def __str__(self):
        return str('%s',self.tag_names[self.bits.b.ID])





class VTP(object):
    def __init__(self):
        self.header = self.Header()
        self.dma_ents = []
    def read(self,f):
        self.header.read(f)
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
    class DMATable(object):
        class DMATableHeader(object):
            def __init__(self):
                self.offset = 0x20
                self.count = 0
                self.magic = 0x2C40
                self.unk = 0
            def read(self,f):
                self.offset = u64(f)
                self.count = u16(f)
                self.magic = u16(f)
                self.unk = u64(f)
            def write(self,f):
                w64(self.offset)
                w16(self.count)
                w16(self.magic)
                w64(self.unk)
        def __init__(self):
            self.TableHeader = self.DMATableHeader()
            self.Offsets = []
        def read(self,f):
            self.TableHeader.read(f)
            ret = f.tell()
            f.seek(self.TableHeader.offset)
            for x in range(self.TableHeader.count):
                tag = u32(f)
                offset = u32(f)
                extraTag = u64(f)
                self.Offsets.append(offset)
            #end Tag why not
            tag = u32(f)
            offset = u32(f)
            extraTag = u64(f)
            f.seek(ret)
