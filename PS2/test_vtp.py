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
        next = y.next
        while(next is not None):
            in_inner += 1
            print("\t%s"%next)
            if(next.data is not None):
                out = open(sys.argv[1] + str("%03i_%03i_%03i.bin" %(outer,inner,in_inner)),'wb')
                out.write(next.data)
            next = next.next