import deflate
import struct
import math
def u8(file):
    return struct.unpack("B", file.read(1))[0]
def u16(file):
    return struct.unpack(">H", file.read(2))[0]
def u32(file):
    return struct.unpack(">I", file.read(4))[0]
def rR(f,o,l):#Read n Return, Takes file,offset,size returns data
    c = f.tell()
    f.seek(o)
    d = f.read(l)
    f.seek(c)
    return d
def w32(file,val):
    file.write(struct.pack(">I", val))
def w16(file,val):
    file.write(struct.pack(">H", val))
def w8(file,val):
    file.write(struct.pack("B", val))

decompress_size = 0
chunk_size = 0x10000

class SEGS(object):
    class ENT(object):
        def __init__(self):
            self.size = 0
            self.dsize = 0
            self.addr = 0
            self.cdata = bytearray()
            self.data = bytearray()
        def read(self,f):
            self.size = u16(f)
            self.dsize = u16(f)
            self.addr = u32(f)
            self.cdata = rR(f,self.addr-1,self.size)
            self.data = deflate.deflate_decompress(self.cdata,chunk_size)
        def write_ent(self,f):
            w16(f,self.size)
            w16(f,self.dsize)
            w32(f,self.addr)
        def add_data(self,d,offset):
            self.data = d
            self.cdata = deflate.deflate_compress(d,7)
            if(len(d) < chunk_size):
                self.dsize = len(d)
            self.addr = offset+1
            self.size = len(self.cdata)
            return len(self.cdata)

    def __init__(self):
        self.ents = []
        self.magic = bytearray('segs','utf-8')
        self.ver = 5
        self.count = 0
        self.dsize = 0
        self.fsize = 0
    def read(self,f):
        self.magic = f.read(4)
        self.ver = u16(f)
        self.count = u16(f)
        self.dsize = u32(f)
        self.fsize = u32(f)
        #self.info.read(f)
        for _a in range(self.count):
            ent = self.ENT()
            ent.read(f)
            self.ents.append(ent)
    def write(self,f):
        f.write(self.magic)
        w16(f,self.ver)
        w16(f,self.count)
        w32(f,self.dsize)
        w32(f,self.fsize)
        for x in self.ents:
            x.write_ent(f)
        for x in self.ents:
            cur = f.tell()
            if(cur%0x10):
                f.seek(cur + (0x10-(cur%0x10)))
            f.write(x.cdata)
        cur = f.tell()
        if(cur%0x10):
            f.seek(cur + (0x10-(cur%0x10))-1)
            w8(f,0)
    def writefile(self,f):
        f.seek(0,2)
        size = f.tell()
        f.seek(0)
        count = math.ceil((size/chunk_size))
        end_size = size - ((count-1)*chunk_size)
        ents = []
        segs_size = 0x10 + (count*8)
        if(segs_size%0x10):
            segs_size+=(0x10-(segs_size%0x10))
        for x in range(count-1):
            ent = self.ENT()
            segs_size += ent.add_data(f.read(chunk_size),segs_size)
            if(segs_size%0x10):
                segs_size+=(0x10-(segs_size%0x10))
            ents.append(ent)
        ent = self.ENT()
        segs_size += ent.add_data(f.read(end_size),segs_size)
        if(segs_size%0x10):
                segs_size+=(0x10-(segs_size%0x10))
        ents.append(ent)

        inseg = SEGS()
        inseg.count = count
        inseg.dsize = size
        inseg.fsize = segs_size
        inseg.ents = ents
        return inseg


        

        