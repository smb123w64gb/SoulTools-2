from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from library import model_fmt_sc2 as sc2m
from library import smd_lib
import mathutils
import math
import copy


class VXTProto(object):
        def __init__(self):
            self.pos = [0.0]*3
            self.nor = [0.0]*3
            self.uvs = [0.0]*2
            self.wght = 1.0 
        def __str__(self):
             rt = ''
             rt += str("POS:%f,%f,%f\n"%(self.pos[0],self.pos[1],self.pos[2]))
             rt += str("NOR:%f,%f,%f\n"%(self.nor[0],self.nor[1],self.nor[2]))
             rt += str("UVS:%f,%f\n"%(self.uvs[0],self.uvs[1]))
             rt += str("WGT:%f\n"%(self.wght))
             return rt
        def __repr__(self):
             return self.__str__()
def euler_to_degrees(roll, pitch, yaw):
    roll_deg = float(roll) * 360.0
    pitch_deg = float(pitch)* 360.0
    yaw_deg = float(yaw)* 360.0
    return roll_deg, pitch_deg, yaw_deg

def degrees_to_radians(roll, pitch, yaw):
    roll_rad = float(roll) * (math.pi / 180.0)
    pitch_rad = float(pitch) * (math.pi / 180.0)
    yaw_rad = float(yaw) * (math.pi / 180.0)
    return roll_rad, pitch_rad, yaw_rad

def radians_to_degrees(roll, pitch, yaw):
    roll_rad = 180.0 * float(roll) / (math.pi)
    pitch_rad = 180.0 * float(pitch) / (math.pi)
    yaw_rad = 180.0 * float(yaw) / (math.pi)
    return roll_rad, pitch_rad, yaw_rad

def applyTransform(vertex,bone_idx,bonez):
    next_bone = bone_idx
    transforms = mathutils.Vector((vertex[0],vertex[1],vertex[2]))
    chain = []
    while(next_bone != 255):
        bon = bonez[next_bone]
        
        chain.append(next_bone)
        next_bone = bon.BoneParentIdx
    chain.reverse()
    onceler = True
    for x in chain:
        bon = bonez[x]
        
        d = euler_to_degrees(bon.Rotation[0],bon.Rotation[1],bon.Rotation[2])
        e = degrees_to_radians(d[0],d[1],d[2])
        e = [x for x in e]
        r = mathutils.Euler((e[0],e[1],e[2]))
        r = r.to_matrix()
        if(bon.boneType == 3 and onceler):
            mat_rotY = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
            mat_rotZ = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
            mat_rotate = (mat_rotY @ mat_rotZ)
            onceler = False
            r.rotate(mat_rotate)
        r.invert()
        
        tra = mathutils.Vector((-bon.StartPositionXYZScale[0],-bon.StartPositionXYZScale[1],-bon.StartPositionXYZScale[2]))
        transforms = transforms + tra
        transforms.rotate(r)
        
    loc = transforms
    return (loc[0],loc[1],loc[2])
def applyTransform_norm(vertex,bone_idx,bonez):
    next_bone = bone_idx
    transforms = mathutils.Vector((vertex[0],vertex[1],vertex[2]))
    chain = []
    while(next_bone != 255):
        bon = bonez[next_bone]
        
        chain.append(next_bone)
        next_bone = bon.BoneParentIdx
    chain.reverse()
    onceler = True
    for x in chain:
        bon = bonez[x]
        
        d = euler_to_degrees(bon.Rotation[0],bon.Rotation[1],bon.Rotation[2])
        e = degrees_to_radians(d[0],d[1],d[2])
        e = [x for x in e]
        r = mathutils.Euler((e[0],e[1],e[2]))
        r = r.to_matrix()
        if(bon.boneType == 3 and onceler):
            mat_rotY = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
            mat_rotZ = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
            mat_rotate = (mat_rotY @ mat_rotZ)
            onceler = False
            r.rotate(mat_rotate)
        r.invert()
        transforms.rotate(r)
        
    loc = transforms
    return (loc[0],loc[1],loc[2])



root = Tk()
tN = 'Soul Calibur II VM_ Tool'

root.geometry("640x480")
VMtest = sc2m.VM()



def tmp():
    pass
def fl_open():
    file_types = [
        ("SC2 Model files", "*.vmx *.vmg"),
        ("Xbox Model files", "*.vmx"),
        ("Gamecube Model", "*.vmg"),
        ("All files", "*.*")
    ]
    # Open the file dialog with filters
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=file_types
    )
    if file_path:
        print(f"Selected file: {file_path}")
        root.title(tN+' File:'+file_path)
        f = open(file_path,'rb')
        global VMtest
        VMtest = sc2m.VM()
        VMtest.read(f)
        f.close()
        cred = VMtest.credits

        usDateTime = f"{cred.month}/{cred.day}/{cred.year} {cred.hour}:{cred.min}:{cred.sec}"

        CreditDate.configure(state="normal")
        CreditDate.delete(1.0,END) 
        CreditDate.insert(1.0, usDateTime)
        CreditDate.configure(state="disabled")

        CreditName.configure(state="normal")
        CreditName.delete(1.0,END) 
        CreditName.insert(1.0, VMtest.credits.name)
        CreditName.configure(state="disabled")
        update_matList()
        update_MeshMenu()
        
    else:
        print("No file selected.")
def fl_save():
    file_types = [
        ("Xbox Model files", "*.vmx"),
        ("All files", "*.*")
    ]
    # Open the file dialog with filters
    file_path = filedialog.asksaveasfilename(
        title="Select a file",
        defaultextension=".vmx",
        filetypes=file_types
    )
    if file_path:
        print(f"Selected file: {file_path}")
        f = open(file_path,'wb')
        VMtest.write(f)
        f.close()
    else:
        print("No file selected.")

def import_smd():
    file_types = [
    ("StudioModel Data", "*.smd"),
    ("All files", "*.*")
    ]
    # Open the file dialog with filters
    file_path = filedialog.askopenfilename(
    title="Select a file",
    filetypes=file_types
    )
    if file_path:
        f = open(file_path,'r')
        inModel = smd_lib.SMD()
        inModel.read(f)
        inModel.sort()
        mesh = []
        riggedBuff = []
        staticBuffPOSNOR = []
        staticBuffUVSCOL = []
        for idy,y in inModel.merged_list.items():
            binds = {}
            vtnr = sc2m.VM.WeightTable.BufferScaleVertex()
            vtnr.Position = applyTransform(y.pos,0,VMtest.boneInfo)
            vtnr.Normal = applyTransform_norm(y.nor,0,VMtest.boneInfo)
            staticBuffPOSNOR.append(vtnr)

            uvcl = sc2m.VM.WeightTable.BufferColorUV()
            uvcl.UV = y.uvs
            staticBuffUVSCOL.append(uvcl)
            
            for idz,z in y.bns.items():
                    vt = VXTProto()
                    vt.pos = y.pos
                    vt.nor = y.nor
                    vt.uvs = y.uvs
                    vt.wght = z
                    binds[idz] = vt
            riggedBuff.append(binds)

        VMtest.wgtTbl.VertexBuff0 = staticBuffUVSCOL
        VMtest.wgtTbl.VertexBuff1 = staticBuffPOSNOR
        VMtest.wgtTbl.VertexBuff2 = staticBuffPOSNOR

        VMtest.matrix_table = VMtest.matrix_table[:1]
        VMtest.materials = VMtest.materials[:1]
        VMtest.materials[0].TextureIdx0 = 0
        VMtest.materials[0].TextureIdx1 = None
        VMtest.materials[0].TextureIdx2 = None
        material_base = copy.deepcopy(VMtest.materials[0])
        material_base.TextureMap1 = None
        VMtest.materials = []
        VMtest.Object_0 = []
        VMtest.Object_1 = []
        VMtest.Object_2 = []

        txIndx = 0
        for xx,idx in inModel.mesh_original.items():
            x:smd_lib.SMD.MVXT = idx
            mesh = x.poly(inModel.merged_list)
            newlayer = sc2m.VM.LayerObjectEntryXbox()
            newlayer.Mesh = mesh
            newlayer.ObjectType = 4
            newlayer.PrimitiveType = 1
            mat = copy.deepcopy(material_base)
            VMtest.materials.append(mat)
            newlayer.MaterialIndex = txIndx
            txIndx += 1
            VMtest.Object_0.append(newlayer)



        boneindx = {}
        for x in VMtest.boneInfo:
            if(x.BoneNameOffset>0):
                boneindx[x.Name] = x


        finalPosWgt = []
        curhigh = 1
        topfour = 4
        curIdx = 0
        wgtz = []
        weghtsub = []
        for xx in riggedBuff:
            if(len(xx)>topfour):
                #BindCOunt / CurVtx / SubVertex
                finalPosWgt[-1][-1][-1].stat = 1
                topfour += 1
            elif(curhigh<len(xx)):
                if(curhigh==4):
                    pass
                else:
                    if(len(weghtsub)):
                        finalPosWgt.append(weghtsub)
                    weghtsub = []
                    curhigh += 1
            wgtz = []
            for idx,x in xx.items():
                
                bone = boneindx[idx]
                updatedPos = applyTransform(x.pos,bone.BoneIdx,VMtest.boneInfo)
                updatedNor = applyTransform_norm(x.nor,bone.BoneIdx,VMtest.boneInfo)
                if(len(xx)>1):
                    updatedPos = [(updatedPos[0]*x.wght),(updatedPos[1]*x.wght),(updatedPos[2]*x.wght)]
                wgt = sc2m.VM.WeightTable.WeightDef()
                wgt.Pos = updatedPos
                wgt.Nor = updatedNor
                wgt.bWgt = x.wght
                wgt.bIdx = bone.BoneIdx
                wgtz.append(wgt)
            weghtsub.append(wgtz)
        finalPosWgt.append(weghtsub)
        if(curhigh==4):
            finalPosWgt[-1][-1][-1].stat = 4


        flatbuffer = []
        totalry = [0,0,0,0]
        idx = 0
        for x in finalPosWgt:
            buf = []
            for y in x:
                totalry[idx] += 1
                for z in y:
                    buf.append(z)
            idx+=1
            flatbuffer.append(buf)
        VMtest.wgtTbl.VertCounts = totalry
        VMtest.wgtTbl.WeightBuffer = flatbuffer
        VMtest.header.WeightTableCount = 1
        update_matList()

def update_matList():
    material_list.delete(0,END)
    for x in range(len(VMtest.materials)):
        material_list.insert(END,str("Mat %02i"%x))
def get_material(event=None):
    selected = material_list.curselection()
    if selected: # If item is selected
        
        mat:sc2m.VM.Material = VMtest.materials[selected[0]]
        if(mat.TextureIdx0 is None):
            matstate[0].set(False)
            matindx[0].config(state=DISABLED)
            matindex[0].set(0)
        else:
            matstate[0].set(True)
            matindx[0].config(state=NORMAL)
            matindex[0].set(mat.TextureIdx0)
        if(mat.TextureIdx1 is None):
            matstate[1].set(False)
            matindx[1].config(state=DISABLED)
            matindex[1].set(0)
        else:
            matstate[1].set(True)
            matindx[1].config(state=NORMAL)
            matindex[1].set(mat.TextureIdx1)
        if(mat.TextureIdx2 is None):
            matstate[2].set(False)
            matindx[2].config(state=DISABLED)
            matindex[2].set(0)
        else:
            matstate[2].set(True)
            matindx[2].config(state=NORMAL)
            matindex[2].set(mat.TextureIdx2)

        print("Selected Item : ",selected[0]) # print the selected item
def update_texture():
    selected = material_list.curselection()
    global VMtest
    mat:sc2m.VM.Material = VMtest.materials[selected[0]]
    for idx,x in enumerate(matstate):
        if(x.get()):
            matindx[idx].config(state=NORMAL)
            match idx:
                case 0:
                    mat.TextureIdx0 = 0
                case 1:
                    mat.TextureIdx1 = 0
                case 2:
                    mat.TextureIdx2 = 0
        else:
            matindx[idx].config(state=DISABLED)
            match idx:
                case 0:
                    mat.TextureIdx0 = None
                case 1:
                    mat.TextureIdx1 = None
                case 2:
                    mat.TextureIdx2 = None
    for idx,x in enumerate(matindex):
            if(matstate[idx].get()):
                match idx:
                    case 0:
                        mat.TextureIdx0 = int(x.get())
                    case 1:
                        mat.TextureIdx1 = int(x.get())
                    case 2:
                        mat.TextureIdx2 = int(x.get())
    get_material()

current_mesh_selected = None
def popup_MeshRightClick(event):
    """action in event of button 3 on tree view"""
    # select row under mouse
    mesh_menu.entryconfig("Move to Diffuse", state="normal")
    mesh_menu.entryconfig("Move to Overlay", state="normal")
    mesh_menu.entryconfig("Move to Alpha", state="normal")
    global current_mesh_selected
    iid = meshview.identify_row(event.y)
    if iid:
        # mouse pointer over item
        meshview.selection_set(iid)
        curItem = iid
        if(len(meshview.item(curItem)['tags'])>0):
            if(meshview.item(curItem)['tags'][0] == 0):
                mesh_menu.entryconfig("Move to Diffuse", state="disabled")
            elif(meshview.item(curItem)['tags'][0] == 1):
                mesh_menu.entryconfig("Move to Overlay", state="disabled")
            elif(meshview.item(curItem)['tags'][0] == 2):
                mesh_menu.entryconfig("Move to Alpha", state="disabled")
            current_mesh_selected = curItem
            mesh_menu.post(event.x_root, event.y_root)            
    else:
        # mouse pointer not over item
        # occurs when items do not fill frame
        # no action required
        pass
def update_MeshMenu(event=None):
    for item in meshview.get_children():
        meshview.delete(item)
    diffuselst = meshview.insert("", END, text="Diffuse(Layer 0)")
    overlaylst = meshview.insert("", END, text="Overlay(Layer 1)")
    alphalst = meshview.insert("", END, text="Alpha(Layer 2)")
    global VMtest
    for idx,x in enumerate(VMtest.Object_0):
        meshview.insert(diffuselst, END, text=str("Mesh_%02i"%idx),tags=0,values=idx)
    for idx,x in enumerate(VMtest.Object_1):
        meshview.insert(overlaylst, END, text=str("Mesh_%02i"%idx),tags=1,values=idx)
    for idx,x in enumerate(VMtest.Object_2):
        meshview.insert(alphalst, END, text=str("Mesh_%02i"%idx),tags=2,values=idx)
def move_MeshMenu(layer_idx):
        meshview.selection_set(current_mesh_selected)
        curItem = current_mesh_selected
        global VMtest
        print(meshview.item(curItem))
        if(meshview.item(curItem)['tags'][0]==0):
            value_move = VMtest.Object_0.pop(meshview.item(curItem)['values'][0])
        elif(meshview.item(curItem)['tags'][0]==1):
            value_move = VMtest.Object_1.pop(meshview.item(curItem)['values'][0])
        elif(meshview.item(curItem)['tags'][0]==2):
            value_move = VMtest.Object_2.pop(meshview.item(curItem)['values'][0])
        match layer_idx:
            case 0:
                VMtest.Object_0.append(value_move)
            case 1:
                VMtest.Object_1.append(value_move)
            case 2:
                VMtest.Object_2.append(value_move)
            case _:
                print("HOW!")
        update_MeshMenu()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=fl_open)
filemenu.add_command(label="Save", command=tmp)
filemenu.add_command(label="Save as...", command=fl_save)
filemenu.add_command(label="Close", command=tmp)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)

Button(text="Open VM_", command=fl_open).grid(row=0, column=0, padx=10, pady=5)
Button(text="Import SMD", command=import_smd).grid(row=1, column=0, padx=10, pady=5)

creddt_reg = Frame(root)
creddt_reg.grid(row=0, column=1)

credn_reg = Frame(root)
credn_reg.grid(row=1, column=1)

dt = Label(creddt_reg, text="Date Created")  
dt.grid(row=0, column=3, padx=10, pady=5) 

cr = Label(credn_reg, text="Created By  ")  
cr.grid(row=1, column=3, padx=10, pady=5) 

CreditDate = Text(creddt_reg, height=1, borderwidth=0,width=20) 
CreditDate.insert(1.0, "")
CreditDate.grid(row=0, column=1, padx=5, pady=5)
CreditDate.configure(state="disabled")

CreditName = Text(credn_reg, height=1, borderwidth=0,width=20) 
CreditName.insert(1.0, "")
CreditName.grid(row=1, column=1, padx=5, pady=5) 
CreditName.configure(state="disabled")

mesh_menu = Menu(root, tearoff=0)
mesh_menu.add_command(label="Move to Diffuse", command=lambda: move_MeshMenu(0))
mesh_menu.add_command(label="Move to Overlay", command=lambda: move_MeshMenu(1))
mesh_menu.add_command(label="Move to Alpha", command=lambda: move_MeshMenu(2))

mesh_lst_frame = Frame(root)
mesh_lst_frame.grid(row=2, column=0)
meshview = ttk.Treeview(mesh_lst_frame)
meshview.heading("#0", text="Mesh Layers")
meshview.bind("<Button-3>", popup_MeshRightClick)

mesh_scrollbar = Scrollbar(mesh_lst_frame, orient=VERTICAL)
mesh_scrollbar.grid(row=0, column=1, sticky="ns")
meshview.config(yscrollcommand = mesh_scrollbar.set)
mesh_scrollbar.config(command = meshview.yview)
diffuselst = meshview.insert("", END, text="Diffuse(Layer 0)")
overlaylst = meshview.insert("", END, text="Overlay(Layer 1)")
alphalst = meshview.insert("", END, text="Alpha(Layer 2)")
meshview.grid(row=0,column=0)


mat_lst_frame = Frame(root)
mat_lst_frame.grid(row=2, column=1)

cr = Label(mat_lst_frame, text="Materials")  
cr.grid(row=0, column=0, padx=10, pady=5) 

material_list = Listbox(mat_lst_frame)
material_list.bind('<<ListboxSelect>>',get_material)
material_list.grid(row=1, column=0)
mat_scrollbar = Scrollbar(mat_lst_frame, orient=VERTICAL)
mat_scrollbar.grid(row=1, column=1, sticky="ns")
material_list.config(yscrollcommand = mat_scrollbar.set)
mat_scrollbar.config(command = material_list.yview)

mat_detail_frm = Frame(root)
mat_detail_frm.grid(row=2, column=2)

matstate = [BooleanVar(value=False),BooleanVar(value=False),BooleanVar(value=False)]
matindex = [IntVar(value=0),IntVar(value=0),IntVar(value=0)]
matendx = []
matindx = []
for x in range(3):
    matendx.append(Checkbutton(mat_detail_frm, text=str("Texture Bind %i"%x),variable=matstate[x],command=update_texture))
    matendx[x].grid(row=x, column=0)
    matindx.append(Spinbox(mat_detail_frm,textvariable=matindex[x], from_=0, to=255, width=6, repeatdelay=500, repeatinterval=100,command=update_texture))
    matindx[x].grid(row=x, column=1)
    matindx[x].config(state=DISABLED)



mainloop()