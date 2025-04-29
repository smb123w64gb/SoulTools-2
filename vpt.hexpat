struct addressTable{
u32 UNK0;
u32 EntryOffset;
u32 UNK1;
u32 UNK2;
};
struct Pallet{
u32 color[256];
};
struct TextureSlice{
u32 stuff[24];
u32 PalletLen;
u32 count;
padding[8];
u16 UNK0;
u16 UNK1;
u32 PalletOffset;
padding[8];
//u8 data[PalletLen] @ PalletOffset;
};
struct TextureEntry{

TextureSlice slices[2];
u32 footer[4];
u32 pal[slices[0].PalletLen] @ slices[1].PalletOffset;
};
struct DimentionEnt{
u32 stuff[16];
};

struct VPT{
u32 Header;
u8 idk;
u8 textureCount;
u16 idk2;
u32 address1;
u32 address2;
u32 address3;
u32 footer;
padding[8];
addressTable textureInfo[textureCount];
u32 paddr[4];
TextureEntry textEnt[textureCount];
DimentionEnt dimmy[textureCount];
//Pallet pallets[textureCount];
};

VPT file @ 0;