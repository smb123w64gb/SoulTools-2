


import dolphin_memory_engine
import os
import time

from ctypes import c_char




def bytes_to_mib(bytes_value):
    mib_value = bytes_value / (1024 * 1024)
    return mib_value

class MemBuff(object):
    def __init__(self,memoryoffset):
        self.MEM_OFFSET = memoryoffset
        self.used = -1
        self.index = 0
        self.name = ''
        self.offset_head = 0
        self.offset_end = 0
        self.space_alloted = 0
        self.space_used = 0
        self.space_left = 0

    def __str__(self,basic = False):
        strpit = ''
        if(self.used==0xFF):
            return 'NO DATA\n'
        strpit += str("Used: %i\t Index: %02i\n"% (self.used,self.index))
        strpit += str("name: %s\n"% self.name)
        strpit += str("Offset Range %s - %s\n"% (hex(self.offset_head),hex(self.offset_end)))
        if(basic):
            strpit += str("Data Used %02.02f MiB / %02.02f MiB\n"% (bytes_to_mib(self.space_used),bytes_to_mib(self.space_alloted)))
            strpit += str("Avalable %02.02f MiB\n"% bytes_to_mib(self.space_left))
        else:
            strpit += str("Data Used %s / %s\n"% (hex(self.space_used),hex(self.space_alloted)))
            strpit += str("Avalable %s\n"% hex(self.space_left))
        return strpit
    def read(self):
        offset = self.MEM_OFFSET
        self.used = dolphin_memory_engine.read_byte(offset)
        offset+=2
        self.index = dolphin_memory_engine.read_byte(offset)
        offset+=2
        strlen = 32
        result = ""
        tmpChar = bytes(c_char(dolphin_memory_engine.read_byte(offset)))
        strlen -=1
        offset+=1
        while ord(tmpChar) != 0 and strlen > 0:
            result += tmpChar.decode("shift_jis")
            tmpChar = bytes(c_char(dolphin_memory_engine.read_byte(offset)))
            strlen -=1
            offset+=1
        self.name = result
        offset += strlen
        self.offset_head = dolphin_memory_engine.read_word(offset)
        offset += 4
        self.offset_end = dolphin_memory_engine.read_word(offset)
        offset += 4
        self.space_alloted = dolphin_memory_engine.read_word(offset)
        offset += 4
        self.space_used = dolphin_memory_engine.read_word(offset)
        offset += 4
        self.space_left = dolphin_memory_engine.read_word(offset)
        offset += 4


base_offset = 0x8034d0ac
arrayOfBuff = []
for x in range(18):
    test = MemBuff(base_offset)
    arrayOfBuff.append(test)
    base_offset += 0x38
dolphin_memory_engine.hook()
while(1):
    total = 0.0
    os.system('cls')
    for test in arrayOfBuff:
        test.read()
        print(test.__str__(True))
        total += bytes_to_mib(test.space_used)
    print("Total Used space %02.02f Mib" % total)
    time.sleep(1)

