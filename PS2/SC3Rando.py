
import ctypes
import os
import platform
import time
import random
from ctypes import c_void_p, c_uint, c_ulong, c_char, c_bool, c_uint64

print("hello world")

# we get the correct library extension per os
lib="libpine_c"
cur_os = platform.system()
if(cur_os == "Linux"):
    lib="libpine_c.so"
elif(cur_os == "Windows"):
    lib="pine_c.dll"
elif(cur_os == "Darwin"):
    lib="libpine_c.dylib"


# we load the library, this will require it to be in the same folder
# refer to bindings/c to build the library.
print("readin dll")
libipc = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),lib),winmode=0)

libipc.pine_pcsx2_new.restype = c_void_p

libipc.pine_read.argtypes = [c_void_p, c_uint, c_char, c_bool]
libipc.pine_read.restype = c_ulong

libipc.pine_write.argtypes = [c_void_p, c_uint, c_uint64 , c_char, c_bool]
libipc.pine_write.restype = None

libipc.pine_get_error.argtypes = [c_void_p]
libipc.pine_get_error.restype = c_uint

libipc.pine_pcsx2_delete.argtypes = [c_void_p]
libipc.pine_pcsx2_delete.restype = None

ipc = libipc.pine_pcsx2_new()


ValidIDs = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x0B,0x0C,0x0D,0x0E,0x0F,0x11,0x12,0x14,0x15,0x16,0x17,0x1A,0x22,0x23,0x24,0x26,0x27,0x28,0x29,0x2A,0x30,0x31,0x32,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x4A,0x4B,0x4C,0x4D,0x4E,0x4F,0x51,0x54]
Address = c_uint(0x4BA062)

value = 0
random.seed(time.time())
while(1):
    os.system('cls')
    print("Transforming into %i" % ValidIDs[value])
    curchar = libipc.pine_read(ipc, Address, c_char(0), False)
    print("Cur char id was:%i"%curchar)
    libipc.pine_write(ipc,Address,ValidIDs[value],c_char(4),False)
    value = random.randint(0,len(ValidIDs)-1)
    time.sleep(10)

