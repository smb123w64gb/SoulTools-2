struct Header{
char MAGIC[4];
u32 size;
u8 unk1;
u8 unk2;
u16 unk3;
u32 unk4;
u32 unk5;
u32 count;
};
struct Entry{
u32 HeaderOffset;
u32 HeaderSize;
u32 DataOffset;
u32 DataSize;
u8 HDR[HeaderSize] @ HeaderOffset;
u8 DATA[DataSize] @ DataOffset;
};
struct MMA{
Header HDR;
Entry ents[HDR.count];
};
be MMA file @ 0;