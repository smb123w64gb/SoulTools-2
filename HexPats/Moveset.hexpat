struct MotHeader {
    /* 0x0000 */ u16 unk0;
    /* 0x0002 */ u16 count;
    /* 0x0004 */ char date[0x20]; // shift-jis encoding
    /* 0x0024 */ u32 unk1; // Magic Hash idk
    /* 0x0028 */ u16 unk2; // start index
    /* 0x002A */ u16 count2; //count for secion
    /* 0x002C */ u32 unk3;
    /* 0x0030 */ u32 entriesOffset;
    /* 0x0034 */ u32 cmdOffset; // byte code data
    /* 0x0038 */ u32 moveinfoOffset; // move info?
    /* 0x003C */ u32 ThrowArray;
    /* 0x0040 */ u32 fileSize;
    /* 0x0044 */ u32 unk4;
    /* 0x0048 */ u32 unk5;
    /* 0x004C */ u16 unk6;
    /* 0x004E */ u16 unk7;
    /* TODO   */
};
struct MotEntry{


    };
struct mot_toc {
        /* 0x0000 */ u16 mot_id;
        /* 0x0002 */ u8 _p0[0x4E];
        /* 0x0034 */ u32 activeFrames;
        /* 0x0038 */ u8 _p1[0x18];
        /* 0x0050 */ u32 block1_ptr; // script
        /* 0x0054 */ u32 block2_ptr;  // damage/frame info?
        /* 0x0058 */ u16 block3_ptr; // & 0xEFFF * 2
        /* 0x005A */ u16 unk1;
        /* 0x005C */ u8 _p2[4];
};

struct Moveset{
MotHeader hdr;
MotEntry entry;

};

Moveset moves @ 0;