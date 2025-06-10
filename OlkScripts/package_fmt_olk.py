import struct,datetime,sys,os

def u8(file):
    return struct.unpack("B", file.read(1))[0]
def u16(file):
    return struct.unpack("<H", file.read(2))[0]
def u32(file):
    return struct.unpack("<I", file.read(4))[0]
def rR(f,o,l):#Read n Return, Takes file,offset,size returns data
    c = f.tell()
    f.seek(o)
    d = f.read(l)
    f.seek(c)
    return d

default_olkName = ['human.olk','stage.olk','cdata.olk','cpudata.olk','motinfo.olk']

class OLK(object):
    class ENT(object):
        def __init__(self):
            self.addr = 0
            self.data = bytearray()
            self.time = datetime.datetime.now()
        def read(self,f):
            self.addr = u32(f)
            size = u32(f)
            self.time = u32(f)
            f.seek(4,1)
            self.data = rR(f,self.addr,size)
    def __init__(self):
        self.files = []
        self.alignment = 2048 #0x800
        self.magic = bytearray('olnk','utf-8')
        self.info = self.ENT()
    def read(self,f):
        count = u32(f)
        self.magic = f.read(4)
        self.alignment = u32(f)
        f.seek(0x14,1)
        #self.info.read(f)
        for _a in range(count):
            ent = self.ENT()
            ent.read(f)
            self.files.append(ent)
            fil = open(default_olkName[_a],'wb')
            fil.write(ent.data)
            fil.close()
            os.utime(default_olkName[_a], (ent.time, ent.time))

olk_file = open(sys.argv[1], "rb")
olk_in = OLK()
olk_in.read(olk_file)
olk_file.close()