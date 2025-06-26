import std.mem;
struct dmaTable{
u32 Tag;
u32 EntryOffset;
padding[8];
};
/** Destination chain tag. */
enum DmaTagType : u64
{
    /** Transfers the QWC qword from the ADDR field, clears the Dn_CHCR.STR to 0, and ends transfer. */
    P2_DMA_TAG_REFE = 0,
    /** Transfers the QWC qword following the tag and reads the succeeding qword as the next tag. */
    P2_DMA_TAG_CNT = 1,
    /** Transfers the QWC qword following the tag and reads the qword of the ADDR field as the next tag. */
    P2_DMA_TAG_NEXT = 2,
    /** Transfers the QWC qword from the ADDR field and reads the qword following the tag as the next tag.  */
    P2_DMA_TAG_REF = 3,
    /** 
     * Transfers the QWC qword from the ADDR field while controlling stalls 
     * and reads the qword following the tag as the next tag.
     * @note Effective only on the VIF1, GIF, and SIF1 channels. 
     */
    P2_DMA_TAG_REFS = 4,
    /** 
     * Transfers the QWC qword following the tag, pushes the next field into 
     * the Dn_ASR register, and reads the qword of the ADDR field as the next tag. 
     * @note Effective only on the VIF0, VIF1, and GIF channels. 
     * Addresses can be pushed up to 2 levels 
     */
    P2_DMA_TAG_CALL = 5,
    /** 
     * Transfers the QWC qword following the tag and reads the 
     * qword of the field popped from the Dn_ASR register as the 
     * next tag. 
     * Transfers the QWC qword following the tag, clears the 
     * Dn_CHCR.STR to 0, and ends transfer when there is no 
     * pushed address. 
     * @note Effective only on the VIF0, VIF1, and GIF channels. 
     */
    P2_DMA_TAG_RET = 6,
    /** Transfers the QWC qword following the tag, clears the Dn_CHCR.STR to 0, and ends transfer. */
    P2_DMA_TAG_END = 7
};
bitfield dma_tag_t
{
    /** Quadword count. */
     QWC : 16;
     PAD : 10;
    /** 
     * Priority Control Enable. 
     * 00 Nothing performed 
     * 01 Reserved 
     * 10 Priority setting disabled (D_PCR.PCE = 0) 
     * 11 Priority setting enabled (D_PCR.PCE = 1) 
     */
     PCE : 2;
    /** Tag ID. (look at DmaTagType) */
     DmaTagType ID : 3;
    /** 
     * Interrupt Request. 
     * 0 No interrupt request 
     * 1 Interrupt request at end of packet transfer 
     */
     IRQ : 1;
    /** 
     * Address. 
     * Address of packet or next tag instruction 
     * (With qword alignment, lower 4 bits become 0.) 
     */
     ADDR : 31;
    /** 
     * Memory/SPR Selection. 
     * 0 Memory address 
     * 1 SPR address 
     */
     SPR : 1;
     OPT1 : 32;
     OPT2 : 32;
};

struct addressTable{

dma_tag_t values[while(std::mem::read_unsigned($, 4) != 0x60000000)];
dma_tag_t end;
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
u8 dmaCount;
u8 textureCount;
u16 idk2;
u32 address1;
u32 address2;
u32 address3;
u32 footer;
padding[8];
addressTable textureInfo[dmaCount];
TextureEntry textEnt[textureCount];
DimentionEnt dimmy[textureCount];
//Pallet pallets[textureCount];
};

VPT file @ 0;