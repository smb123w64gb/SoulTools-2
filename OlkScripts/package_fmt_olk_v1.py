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

class OLK(object):
    class ENT(object):
        def __init__(self):
            self.addr = 0
            self.data = bytearray()
        def read(self,f,offset=0):
            self.addr = u32(f)
            size = u32(f)
            f.seek(8,1)
            self.data = rR(f,self.addr+offset,size)
    def __init__(self):
        self.files = []
        self.magic = bytearray('olnk','utf-8')
        self.info = self.ENT()
    def read(self,f,output):
        count = u32(f)
        self.magic = f.read(4)
        f.seek(0x10)
        header = self.ENT()
        header.read(f)
        outDir = str(output+"_Extract/")
        os.makedirs(outDir, exist_ok=True)
        for _a in range(count):
            ent = self.ENT()
            ent.read(f,header.addr)
            #self.files.append(ent)
            if(len(ent.data)):
                fil = open(outDir + str("%04i" % _a) + ".bin",'wb')
                fil.write(ent.data)
                fil.close()

olk_file = open(sys.argv[1], "rb")
olk_in = OLK()
olk_in.read(olk_file,sys.argv[1])
olk_file.close()