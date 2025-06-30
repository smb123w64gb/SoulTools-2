#Just a libary to injest smd for now

class SMD(object):
    def __init__(self):
        self.mesh_original = {}
        self.bones = []
    def read(self,f):
        mode = 0
        dict_entry_name = ""
        for x in f.readlines():
            if(x.find("end") == 0):
                mode = 0
            if(mode == 1):
                print(str(x.split()[1]).replace("\"",""))
            if(x.find("nodes") == 0):
                mode = 1
                print(x)
            