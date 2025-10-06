import struct,sys,os

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

class PAR(object):
    def __init__(self):
        self.files = []
    def read(self,f):
        magic = f.read(3)
        subver = u8(f)
        if(subver == 2):
            ver = u32(f)
        else:
            ver = u8(f)
        align = 0x20 if ver == 2 else 0x80
        count = u32(f)
        smth = u32(f)
        f.seek(0x10 % f.tell())
        mappings = []
        for _a in range(count):
            mappings.append(u32(f))
        ret = f.tell()
        f.seek(2,0)
        eof = f.tell()
        mappings.append(eof)
        f.seek(ret)
        sizes = []
        for a in range(count):
            sizes.append(mappings[a+1]-mappings[a])
        mappings.pop()
        for idx,a in enumerate(mappings):
            f.seek(a)
            self.files.append(f.read(sizes[idx]))
pkg_file = open(sys.argv[1], "rb")
pkg_in = PAR()
pkg_in.read(pkg_file)
pkg_file.close()
outDir = str(sys.argv[1]+"_Extract/")
os.makedirs(outDir, exist_ok=True)
for idx,x in enumerate(pkg_in.files):
    fil = open(outDir + str("%04i" % idx) + ".bin",'wb')
    fil.write(x)
    fil.close()