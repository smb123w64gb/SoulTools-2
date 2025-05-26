import texture_fmt_sc2
import sys,os,struct

def u32le(file):
    return struct.unpack("<I", file.read(4))[0]

newTex = texture_fmt_sc2.VTX()

files = os.listdir(sys.argv[1])
files = [ fi for fi in files if fi.endswith(".dds") ]
for x in files:
    dds = open(sys.argv[1] + '\\' + x, "rb")
    dds.seek(0xC)
    width = u32le(dds)
    height = u32le(dds)
    dds.seek(0x1C)
    mipcount = u32le(dds)
    dds.seek(0x54)
    dds_textType = u32le(dds)
    format = texture_fmt_sc2.D3DFORMAT.D3DFMT_DXT1
    if(dds_textType == 894720068):
        format = texture_fmt_sc2.D3DFORMAT.D3DFMT_DXT4
    dds.seek(0x80)
    data = dds.read()
    newTex.addTexture(width,height,data,mipcount,format)

vxt_file = open(sys.argv[2], "wb")
newTex.write(vxt_file)
vxt_file.close()