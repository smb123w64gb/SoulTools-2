#pragma endian little

#pragma loop_limit 999999999


#ifdef __IMHEX__
    import hex.dec;
#endif


import std.io;
import type.color;
u8 clipping_u = 0;

enum FmtTXVFlag : u32
        {
            BIT01 = 1 << 0,
            CLAMP = 1 << 1,
            BIT03 = 1 << 2,
            BIT04 = 1 << 3,
            TWOSIDED = 1 << 4,
            BIT06 = 1 << 5,
            BIT07 = 1 << 6,
            BIT08 = 1 << 7,
            SPEC = 1 << 8,
            BIT10 = 1 << 9,
            BIT11 = 1 << 10,
            BIT12 = 1 << 11,
            BIT13 = 1 << 12,
            BIT14 = 1 << 13
        };
enum ImageTypeXBOX : u32
{
/*
	Xbox1 D3DFORMAT notes
	---------------------

	The Xbox1 D3DFORMAT type consists of 4 different format categories :
	1. Swizzled (improves data locality, incompatible with native Direct3D)
	2. Compressed (DXT compression, giving 4:1 reduction on 4x4 pixel blocks)
	3. Linear (compatible with native Direct3D)
	4. Depth (Fixed or Floating point, stored Linear or Swizzled)

	Requirements\Format      Swizzled  Compressed  Linear  Depth   Notes

	Power-of-two required ?  YES       YES         NO      NO
	Mipmap supported ?       YES       YES         NO      YES     Linear has MipmapLevels = 1
	CubeMaps supported ?     YES       YES         NO      NO      Cubemaps have 6 faces
	Supports volumes ?       YES       YES         NO      NO      Volumes have 3 dimensions, Textures have 2
	Can be a rendertarget ?  YES       YES         YES     LINEAR  Depth buffers can only be rendered to if stored Linear

	Implications :
	- CubeMaps must be square
	- Volumes cannot be cube mapped and vice versa

	Maximum dimensions :
	2D : 4096 x 4096 (12 mipmap levels)
	3D : 512 x 512 x 512 (9 mipmap levels)

*/

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

	D3DFMT_INDEX16 = 101/*=D3DFMT_INDEX16*/, // Dxbx addition : Not an Xbox format, used internally

	D3DFMT_UNKNOWN = 0xFFFFFFFF - 3,  // Unique declaration to make overloads possible
};




struct tVectorColorb {
  u8 R;
  u8 G;
  u8 B;
  u8 A;
} [[ color(std::format("{:02X}{:02X}{:02X}", R, G, B))]];





struct palletData{
u32 PaletteOffset;
u32 PaletteCount;
padding[4];
type::RGBA8 data[PaletteCount] @ PaletteOffset;
};

struct textureData{
    u32 TexturePaletteOffset;
    FmtTXVFlag Flags;
    u32 Unk1;
    if(clipping_u == 2){
    u16 HeightVisible;
    u16 WidthVisible;
    }
    u32 TextureDataOffset;
    ImageTypeXBOX ImageType;
    u16 Height;
    u16 Width;
    u32 MipMapCount;
    padding[4];
    palletData pltData @ TexturePaletteOffset;
    u8 data[Height*Width] @ TextureDataOffset;
}[[hex::visualize("bitmap", data, Width, Height,pltData.data)]];



struct VXT{
    char MAGIC[4];
    
    u8 clipping;
    clipping_u = clipping;
    
    u8 unk01;
    u8 unk02;
    padding[1];
    u32 TextureCount;
    u32 HeaderLen;
    u32 HeaderBlockSize;
    textureData txtData[TextureCount];
    
};


VXT texture @ 0;