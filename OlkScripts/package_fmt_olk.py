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
default_olkName.reverse()
class OLK(object):
    class ENT(object):
        def __init__(self):
            self.addr = 0
            self.data = bytearray()
            self.time = datetime.datetime.now()
        def read(self,f,off):
            self.addr = u32(f)
            size = u32(f)
            self.time = u32(f)
            f.seek(4,1)
            self.data = rR(f,off+self.addr,size)
    def __init__(self):
        self.files = []
        self.alignment = 2048 #0x800
        self.magic = bytearray('olnk','utf-8')
        self.info = self.ENT()
    def read(self,f):
        count = u32(f)
        self.magic = f.read(4)
        self.alignment = u32(f)
        u32(f)
        #f.seek(0x14,1)
        self.info.read(f,0)
        for _a in range(count):
            ent = self.ENT()
            ent.read(f,self.info.addr)
            self.files.append(ent)
            

olk_file = open(sys.argv[1], "rb")

OutDir = sys.argv[1].split('.')[0] + '\\'
os.makedirs(OutDir, exist_ok=True)
olk_in = OLK()
olk_in.read(olk_file)
olk_file.close()

#Root First
for _a,ent in enumerate(olk_in.files):
    if(len(ent.data)):
        fil = open(OutDir+default_olkName[_a],'wb')
        fil.write(ent.data)
        fil.close()
        os.utime(OutDir+default_olkName[_a], (ent.time, ent.time))
for filez in default_olkName:
    olk_file = open(OutDir+filez, "rb")
    subolk = OLK()
    subolk.read(olk_file)
    olk_file.close()
    SubDir = OutDir +filez.split('.')[0] +'\\'
    os.makedirs(SubDir, exist_ok=True)
    for _a,ent in enumerate(subolk.files):
        if(len(ent.data)):
            fil = open(SubDir+str('File%04i.bin'%_a),'wb')
            fil.write(ent.data)
            fil.close()
            os.utime(SubDir+str('File%04i.bin'%_a), (ent.time, ent.time))