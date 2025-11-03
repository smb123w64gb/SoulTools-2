import vpt_lib

f = open(r"C:\Users\smb123w64gb\Documents\artifacts\Mitsu\char.vmp.vxt",'rb')
vpt = vpt_lib.VTP()
vpt.read(f)


print(vpt.header)
for x in vpt.dma_ents:
    for y in x.DMAChains:
        print(y)