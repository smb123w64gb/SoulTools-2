import texture_fmt_sc2
import sys,os,struct
import swizzle

def pilPal_RGBA(arr):
    colors = []
    for x in range(int(len(arr)/3)):
        colors.append(struct.unpack("<I",(struct.pack("BBBB", arr[2+(x*3)],arr[1+(x*3)],arr[0+(x*3)],0xFF)))[0])
    return colors

from PIL import Image

png = Image.open(sys.argv[1])

width = png.width
height = png.height
mipcount = 1
format = texture_fmt_sc2.D3DFORMAT.D3DFMT_P8
pallet = pilPal_RGBA(png.getpalette())
data = bytearray()
firstpass = []
for x in range(width):
    for y in range(height):
        firstpass.append(png.getpixel((y,x)))
png.close()
unsizzled = swizzle.swizzle_rect(firstpass,width,height,width,1)

for x in unsizzled:
    data += struct.pack("B",x)



#vxt_file = open(sys.argv[2], "rb")

newTex = texture_fmt_sc2.VTX()
#newTex.read(vxt_file)
#vxt_file.close()




newTex.addTexture(width,height,data,mipcount,format,pallet)

vxt_file = open(sys.argv[2], "wb")
newTex.write(vxt_file)
vxt_file.close()