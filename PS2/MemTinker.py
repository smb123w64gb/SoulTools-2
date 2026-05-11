from tkinter import *
from tkinter import filedialog
from tkinter import ttk


import mathutils
import math
import copy





root = Tk()
tN = 'Soul Calibur III MEMTool'

root.geometry("640x480")




def tmp():
    pass
def fl_open():
    file_types = [
        ("SC3 PS2 Elf files", "*.16"),
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
        ("SC3 PS2 Elf files", "*.16"),
        ("All files", "*.*")
    ]
    # Open the file dialog with filters
    # Also switch ext from imported file
    file_path = filedialog.asksaveasfilename(
        title="Select a file",
        defaultextension=".16",
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
creddt_reg = Frame(root)
creddt_reg.grid(row=0, column=0)


mainloop()