struct mothdr{
u16 maxFrames;
u16 numBytes;
u32 unk2;//unk + BaseRY(u16 + u16)
u64 unk3;//Bitflags + Weapon Matrixrelated
u16 unk4;
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
motion test @ 0;