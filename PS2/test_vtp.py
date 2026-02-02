import vpt_lib
import sys

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
            if(next.data is not None and next.bits.ID == vpt_lib.DMA_Tag_Type.P2_DMA_TAG_CNT.value):
                for chunk in (next.data[i:i+0x10] for i in range(0,len(next.data),0x10)):
                    testronly = vpt_lib.Gif_Tag()
                    testronly.readbuf(chunk)
                    print(testronly)
            next = next.next