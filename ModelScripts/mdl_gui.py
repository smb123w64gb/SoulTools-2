from tkinter import *
from tkinter import filedialog
from library import model_fmt_sc2

root = Tk()

VMtest = model_fmt_sc2.VM()

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
        lbl.config(text=file_path)
        f = open(file_path,'rb')
        VMtest.read(f)
        lbl2.config(text=VMtest.boneInfo[0].Name)
        f.close()
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

lbl = Label(root, text=" ")  
lbl.pack()  
lbl2 = Label(root, text=" ")  
lbl2.pack()  

Button(text="Import SMD", command=tmp).pack()





mainloop()