from tkinter import *
from tkinter import filedialog
from tkinter import ttk


import mathutils
import math
import copy





root = Tk()
tN = 'Soul Calibur II VM_ Tool'

root.geometry("640x480")




def tmp():
    pass
def fl_open():
    file_types = [
        ("SC2 PS2 files", "*.vtp *.vmp *.unk"),
        ("PS2 Texture file", "*.vtp"),
        ("Ps2 Model file", "*.vmp"),
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
        # More
        
    else:
        print("No file selected.")
def fl_save():
    file_types = [
        ("PS2 Model file", "*.vmp"),
        ("PS2 Texture file", "*.vtp"),
        ("All files", "*.*")
    ]
    # Open the file dialog with filters
    # Also switch ext from imported file
    file_path = filedialog.asksaveasfilename(
        title="Select a file",
        defaultextension=".vtp",
        filetypes=file_types
    )
    if file_path:
        print(f"Selected file: {file_path}")
        f = open(file_path,'wb')
        #VMtest.write(f)
        f.close()
    else:
        print("No file selected.")



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


mainloop()