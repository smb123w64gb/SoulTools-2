import vpt_lib
import sys
import os
f = open(sys.argv[1],'rb')
vpt = vpt_lib.VTP()
vpt.read(f)


print(vpt.header)
outer = 0


for x in vpt.dma_ents:
    outer += 1
    inner = 0
    for y in x.DMAChains:
        inner += 1
        in_inner = 0
        print(y)
        next : vpt_lib.Dma_Tag = y.next
        while(next is not None):
            
            in_inner += 1
            print("\t%s"%next)
            
            if(next.data is not None and next.bits.ID == vpt_lib.DMA_Tag_Type.P2_DMA_TAG_REF.value):
                curFolder = str("%s_extract\\%03i\\" % (sys.argv[1],inner))
                os.makedirs(curFolder, exist_ok=True)
                out = open(curFolder+str("%02i.bin" % in_inner),'wb')
                out.write(next.data)
            
            print(next)
            next = next.next