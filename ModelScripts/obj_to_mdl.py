import sys
obj_file = open(sys.argv[1], "r")

verts = []
norms = []
texcr = []

prepol = []
pol = []

for x in obj_file.readlines():
    #print(x)
    if(x.find('o ') == 0):
        if(len(pol)):
            prepol.append(pol)
        pol = []
    
    if(x.find('v ') == 0):
        texVert = x.split()[1:4]
        vert = []
        for y in texVert:
            vert.append(float(y))
        verts.append(vert)
    if(x.find('vn ') == 0):
        texVert = x.split()[1:4]
        vert = []
        for y in texVert:
            vert.append(float(y))
        norms.append(vert)
    if(x.find('vt ') == 0):
        texVert = x.split()[1:3]
        vert = []
        for y in texVert:
            vert.append(float(y))
        texcr.append(vert)
    if(x.find('f ') == 0):
        poltri = x.split()[1:4]
        politer = []
        for y in poltri:
            tmp = y.split("/")
            ooffi = []
            for z in tmp:
                ooffi.append(int(z))
            politer.append(ooffi)
        pol.append(politer)
prepol.append(pol)

print(prepol[1])