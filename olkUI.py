from tkinter import *

default_olkName = ['human.olk','stage.olk','cdata.olk','cpudata.olk','motinfo.olk']
entry_count = [3,7,8,9,20]

def changeOLK(e):
    file_lst.delete(0,'end')
    idx = -1
    for item in olk_lst.curselection():
      idx = item

    for x in range(entry_count[idx]):
        file_lst.insert(-1,x)
    file_lst.config(yscrollcommand=scrollbar_file.set(0,0))


root = Tk()

scrollbar_olk = Scrollbar(root)
scrollbar_olk.pack(side=RIGHT, fill=Y)
olk_lst = Listbox(root, yscrollcommand=scrollbar_olk.set)
olk_lst.bind("<<ListboxSelect>>", changeOLK)
for n in default_olkName:
    olk_lst.insert(-1,n)
olk_lst.pack(side=LEFT, fill=BOTH)
scrollbar_olk.config(command=olk_lst.yview)

scrollbar_file = Scrollbar(root)
scrollbar_file.pack(side=RIGHT, fill=Y)
file_lst = Listbox(root, yscrollcommand=scrollbar_file.set)
file_lst.pack(side=LEFT, fill=BOTH)
scrollbar_file.config(command=file_lst.yview)


mainloop()