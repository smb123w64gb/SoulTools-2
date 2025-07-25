import zlib
#Just a libary to injest smd for now
def str_to_float(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

class SMD(object):
    class SVXT(object):
        def __init__(self):
            self.pos = [0.0]*3
            self.nor = [0.0]*3
            self.uvs = [0.0]*2
            self.bns = {}
            self.hash = 0
        def read(self,in_line,bones):
            self.hash = zlib.crc32(bytes(in_line,'ascii'))
            split = in_line.split()[1:]
            self.pos = str_to_float(split[:3])
            self.nor = str_to_float(split[3:6])
            self.uvs = str_to_float(split[6:8])
            bone_count = int(split[8])
            bonz = split[9:]
            totalwgt = 0.0
            for x in range(bone_count):
                totalwgt += float(bonz[(x*2)+1])
                self.bns[bones[int(bonz[x*2])]] = float(bonz[(x*2)+1])
    class MVXT(object):
        def __init__(self):
            self.keys = {} #To optimize for CRC checks
            self.idxs = [] #To create the mesh
        def add(self,in_vxts):
            self.keys[in_vxts.hash] = in_vxts
            self.idxs.append(in_vxts.hash)
        
        def poly(self,merge):
            poly_out = []
            listy = list(merge)
            for x in self.idxs:
                poly_out.append(listy.index(x))
            return poly_out
    def __init__(self):
        self.merged_list = {}
        self.mesh_original = {}
        self.bones = []
    def sort(self):
            sortkey = sorted(self.merged_list.items(), key=lambda kez: len(kez[1].bns))
            self.merged_list = dict(sortkey)
    def read(self,f):
        mode = 0
        dict_entry_name = ""
        tri = 0
        for x in f.readlines():
            if(x.find("end") == 0):
                mode = 0
            if(mode == 1):
                self.bones.append(str(x.split()[1]).replace("\"",""))
            if(mode == 2):
                if(tri == 0):
                    dict_entry_name = x
                    if x in self.mesh_original:
                        pass
                    else:
                        self.mesh_original[x] = self.MVXT()
                else:
                    vtx = self.SVXT()
                    vtx.read(x,self.bones)
                    self.mesh_original[dict_entry_name].add(vtx)
                    if(tri == 3):
                        tri = -1
                tri += 1  
            if(x.find("nodes") == 0):
                mode = 1
            if(x.find("triangles")==0):
                mode = 2
        for xx,idx in self.mesh_original.items():
            self.merged_list.update(idx.keys)