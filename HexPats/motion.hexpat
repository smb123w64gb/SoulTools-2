struct mothdr{
u16 maxFrames;
u16 numBytes;
u32 unk2;//unk + BaseRY(u16 + u16)
u64 unk3;//
u16 unk4;
u8 unk5[10];
u16 dataEntryCount;
u16 trueCount = (dataEntryCount >> 1) - 1;
u16 dataEntrys[trueCount];
u16 datahdr[(numBytes>>1)];
u8 data[(dataEntrys[0]-numBytes)];
};
struct motionHdrPointer{
mothdr * offset : u32;
};
struct header{
u32 count;
u32 unk;
//u32 newoffset;//SC1 only
motionHdrPointer offsets[count];
};

struct motion{
header hdr;
};
motion test @ 0; //add be for GC/X360/PS3