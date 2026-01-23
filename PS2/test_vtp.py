import vpt_lib
import sys

f = open(sys.argv[1],'rb')
vpt = vpt_lib.VTP()
vpt.read(f)


print(vpt.header)
for x in vpt.dma_ents:
    for y in x.DMAChains:
        print(y)
        next = y.next
        while(next is not None):
            print("\t%s"%next)
            next = next.next