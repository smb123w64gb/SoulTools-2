enum console : u8 {
    UNK0     = 0,
    UNK1     = 1,
    UNK2     = 2,
    GAMECUBE = 3,
    XBOX     = 4
};

enum modelContent : u8 {
    STAGE     = 0,
    CHARACTER = 1,
    WEAPON    = 2
};

enum meshXboxContent : u16 {
    STATICXBOX  = 0,
    SKINNEDXBOX = 4
};

enum meshGCNContent : u8 {
    STATICGCN  = 2, //(2, 2, 2, 2)
    SKINNEDGCN = 3, //(3, 3, 2, 3)  //(3, 3, 3, 3)
};

enum primativeXbox : u16 {
    TRIANGLESTRIP = 0,
    TRIANGLELIST  = 1
};

enum primativeGCN : u8 {
    PACKEDTRIANGLELIST  = 0x90,
    PACKEDTRIANGLESTRIP = 0x98
};

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

enum imageTypeXBOX : u32{
	// Xbox D3DFORMAT types :
	// See https://wiki.beyondunreal.com/Legacy:Texture_Format

	// Swizzled Formats

	D3DFMT_L8 = 0x00,
	D3DFMT_AL8 = 0x01,
	D3DFMT_A1R5G5B5 = 0x02,
	D3DFMT_X1R5G5B5 = 0x03,
	D3DFMT_A4R4G4B4 = 0x04,
	D3DFMT_R5G6B5 = 0x05,
	D3DFMT_A8R8G8B8 = 0x06,
	D3DFMT_X8R8G8B8 = 0x07,
	D3DFMT_X8L8V8U8 = 0x07, // Alias

	D3DFMT_P8 = 0x0b, // 8-bit Palletized

	D3DFMT_A8 = 0x19,
	D3DFMT_A8L8 = 0x1a,
	D3DFMT_R6G5B5 = 0x27,
	D3DFMT_L6V5U5 = 0x27, // Alias

	D3DFMT_G8B8 = 0x28,
	D3DFMT_V8U8 = 0x28, // Alias

	D3DFMT_R8B8 = 0x29,
	D3DFMT_D24S8 = 0x2a,
	D3DFMT_F24S8 = 0x2b,
	D3DFMT_D16 = 0x2c,
	D3DFMT_D16_LOCKABLE = 0x2c, // Alias

	D3DFMT_F16 = 0x2d,
	D3DFMT_L16 = 0x32,
	D3DFMT_V16U16 = 0x33,
	D3DFMT_R5G5B5A1 = 0x38,
	D3DFMT_R4G4B4A4 = 0x39,
	D3DFMT_A8B8G8R8 = 0x3A,
	D3DFMT_Q8W8V8U8 = 0x3A, // Alias

	D3DFMT_B8G8R8A8 = 0x3B,
	D3DFMT_R8G8B8A8 = 0x3C,

	// YUV Formats

	D3DFMT_YUY2 = 0x24,
	D3DFMT_UYVY = 0x25,

	// Compressed Formats

	D3DFMT_DXT1 = 0x0C, // opaque/one-bit alpha
	D3DFMT_DXT2 = 0x0E, // Alias for D3DFMT_DXT3
	D3DFMT_DXT3 = 0x0E, // linear alpha
	D3DFMT_DXT4 = 0x0F, // Alias for D3DFMT_DXT5
	D3DFMT_DXT5 = 0x0F, // interpolated alpha

	// Linear Formats

	D3DFMT_LIN_A1R5G5B5 = 0x10,
	D3DFMT_LIN_R5G6B5 = 0x11,
	D3DFMT_LIN_A8R8G8B8 = 0x12,
	D3DFMT_LIN_L8 = 0x13,
	D3DFMT_LIN_R8B8 = 0x16,
	D3DFMT_LIN_G8B8 = 0x17,
	D3DFMT_LIN_V8U8 = 0x17, // Alias

	D3DFMT_LIN_AL8 = 0x1b,
	D3DFMT_LIN_X1R5G5B5 = 0x1c,
	D3DFMT_LIN_A4R4G4B4 = 0x1d,
	D3DFMT_LIN_X8R8G8B8 = 0x1e,
	D3DFMT_LIN_X8L8V8U8 = 0x1e, // Alias

	D3DFMT_LIN_A8 = 0x1f,
	D3DFMT_LIN_A8L8 = 0x20,
	D3DFMT_LIN_D24S8 = 0x2E,
	D3DFMT_LIN_F24S8 = 0x2f,
	D3DFMT_LIN_D16 = 0x30,
	D3DFMT_LIN_F16 = 0x31,
	D3DFMT_LIN_L16 = 0x35,
	D3DFMT_LIN_V16U16 = 0x36,
	D3DFMT_LIN_R6G5B5 = 0x37,
	D3DFMT_LIN_L6V5U5 = 0x37, // Alias

	D3DFMT_LIN_R5G5B5A1 = 0x3D,
	D3DFMT_LIN_R4G4B4A4 = 0x3e,
	D3DFMT_LIN_A8B8G8R8 = 0x3f,
	D3DFMT_LIN_B8G8R8A8 = 0x40,
	D3DFMT_LIN_R8G8B8A8 = 0x41,

	D3DFMT_VERTEXDATA = 0x64,

	D3DFMT_INDEX16 = 101,
};

enum textureMapType : u16{
    UNKTT0   = 0,
    DIFFUSE  = 1,
    EFFECTS  = 2,
    ANIMATE  = 3,
    UNKTT    = 4,
    SPECBALL = 5
};

enum materialTableCull : u8{
    DRAWNBOTHSIDES = 0,
    DRAWNONESIDE   = 8
};

bitfield fmtTXV_FLAG{
    BIT01   : 1;  
    CLAMP   : 1;  
    BIT03   : 1;  
    BIT04   : 1;  
    TWOSIDED: 1;  
    BIT06   : 1;  
    BIT07   : 1;  
    BIT08   : 1; 
    SPEC    : 1;  
    BIT10   : 1;
    BIT11   : 1;
    BIT12   : 1;
    BIT13   : 1;
    BIT14   : 1;
};

struct tVector4b{
    u8 X;
    u8 Y;
    u8 Z;
    u8 W;
}[[static,name(std::format("{}{}{}{}", X, Y, Z, W))]];

struct tVectorColorb {
  u8 R   [[color("FF0000")]];
  u8 G [[color("00FF00")]];
  u8 B  [[color("0000FF")]];
  u8 A;
} [[static, color(std::format("{:02X}{:02X}{:02X}", R, G, B))]];

struct tFace{
    u16 X;
    u16 Y;
    u16 Z;
}[[static,name(std::format("{}{}{}", X, Y, Z))]];

bitfield tDimension{
    X : 10;
    Y : 10;
    imagetype : 12;
}[[static,name(std::format("imagetype{}, X: {}, Y:{}",imagetype, X, Y))]];

struct tVectorUVf{
    float X;
}[[static,name(std::format("{%6.3f},{%6.3f}", X, ((X * -1)+1)))]];

struct tVector2f{
    float X;
    float Y;
}[[static,name(std::format("{%6.3f},{%6.3f}", X, Y))]];

struct tVector3f{
    float X;
    float Y;
    float Z;
}[[static,name(std::format("{%6.3f},{%6.3f},{%6.3f}", X, Y,Z))]];

struct tVector4f{
    float X;
    float Y;
    float Z;
    float W;
}[[static,name(std::format("{%6.3f},{%6.3f},{%6.3f},{%6.3f}", X, Y, Z, W))]];

#pragma endian little

import std.io;

struct mdl_header{
    char MAGIC[4];
    if(MAGIC == "VMG\x2E") {
        std::print("Big time!");
        #pragma endian big
        }
    console ConsoleVersion;
    u32 unk;
    modelContent Contents;
        u16 MatricesCount;
    u16 Objects0Count;
    u16 Objects1Count;
    u16 Objects2Count;
    u16 BonesCount;
    u16 MaterialsCount;
    u16 MeshCount; // always 1?
    u32 TextureTableOffset;
    u32 MaterialOffset;
    u32 TextureMapOffset;
    u32 MatrixTableOffset;
    u32 ukn_MatrixTableOffset;
    u32 Object0Offset;
    u32 Object1Offset;
    u32 Object2Offset;
    u32 WeightTableOffset;
    u32 ukn01_offset;
    u32 BoneOffset;
    u32 BoneNameOffset;
    u32 BoneHeaderOffset;
};

struct vxt_header{
char MAGIC[4];
u8 type;
u8 flag0;
u8 flag1;
u8 padding;
u32 TexRowCount;
};

mdl_header SC2_MDL @0;






