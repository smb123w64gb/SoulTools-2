#pragma endian big

import std.io;

enum imageTypeGCN : u32 {
    I4     = 0,  //(4 bit intensity, 8x8 tiles)
    I8     = 1,  //(8 bit intensity, 8x4 tiles)
    IA4    = 2,  //(4 bit intensity with 4 bit alpha, 8x4 tiles)
    IA8    = 3,  //(8 bit intensity with 8 bit alpha, 4x4 tiles)
    RGB565 = 4,  //(4x4 tiles)
    RGB5A3 = 5,  //(*) (4x4 tiles)
    RGBA8  = 6,  //(4x4 tiles in two cache lines - first is AR and second is GB)
    CI4    = 8,  //(4 bit color index, 8x8 tiles)
    CI8    = 9,  //(8 bit color index, 8x4 tiles)
    C14X2  = 10, //(14 bit color index, 4x4 tiles)
    CMPR   = 14, //(S3TC compressed, 2x2 blocks of 4x4 tiles)
    XFB    = 15, // 0x0F
    UNK16  = 16  // 0x10
};


fn imageSizeGCN(u32 num) {
        match ( num ) 
        {
            (2   )   : return 2 << 5; // 8 x 8 
            (4   )   : return 2 << 6; // 16 x 8 
            (8   )   : return 2 << 7; // 32 x 16 
            (16  )   : return 2 << 8; // 32 x 32 
            (32  )   : return 2 << 9; // 64 x 32
            (64  )   : return 2 << 10; // 64 x 64
            (128 )   : return 2 << 11; // 128 x 64
            (256 )   : return 2 << 12; // 128 x 128
            (512 )   : return 2 << 13; // 256 x 128
            (1024)   : return 2 << 14; // 256 x 256
            (2048)   : return 2 << 15; // 512 x 256
            (4096)   : return 2 << 16; // 512 x 512
            (_   )   : return -1;
        }
};
bitfield tDimension{
    X : 10;
    Y : 10;
    imagetype : 12;
}[[static,name(std::format("imagetype{}, X: {}, Y:{}",imagetype, X, Y))]];

struct tVectorColorb {
  u8 R   [[color("FF0000")]];
  u8 G [[color("00FF00")]];
  u8 B  [[color("0000FF")]];
  u8 A;
} [[static, color(std::format("{:02X}{:02X}{:02X}", R, G, B))]];
struct textureDataSlice{

    u32 unk1;
    u16 unk2;
    u16 unk3;
    tDimension Dimensions;
    u32 CLUTOffset;
    u16 unk4;
    u16 unk5;
    imageTypeGCN ImageType;
    u32 unk6;
    u32 unk7;
};


struct textureData{
    u32 TexturePaletteOffset;
    textureDataSlice slices[2];
};

struct VGT{
    char MAGIC[4];
    
    u32 unk0;
    
    u32 TexCount;
    u32 unk1;
    u32 HeaderLen;
    u32 HeaderBlockSize;
    textureData txtData[TexCount];
};

VGT texture @ 0;