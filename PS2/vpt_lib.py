import struct

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


class VTX(object):
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
