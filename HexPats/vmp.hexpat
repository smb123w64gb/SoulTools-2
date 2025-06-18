import std.io;
struct tVector4f{
    float X;
    float Y;
    float Z;
    float W;
}[[static,name(std::format("{},{},{},{}", X, Y, Z, W))]];
struct tVector3f{
    float X;
    float Y;
    float Z;
}[[static,name(std::format("{},{},{}", X, Y,Z))]];

struct Header{
    u32 Type;
    u8 Unk04;
    u8 Unk05;
    u8 Unk06;
    u8 Unk07;
    u16 Object1Count;
    u16 BoneCount;
    u32 Unk0C;
    u32 BoneOffset;
    u32 Unk10;
    u32 Object1Offset;
    u32 Unk18;
    u32 Unk1C;
    u32 BoneHeaderOffset;
};
struct boneInfo { // bone positions relative to its parent
    tVector4f EndPositionXYZScale;
    tVector4f StartPositionXYZScale;
    tVector3f Rotation; // eulerangles, degrees (n*360)
    u32 BoneNameOffset;
    tVector3f ukn_bone1;
    u8 ukn_bone2;
    u8 BoneParentIdx;
    u8 BoneIdx; // used for name look up?
    u8 ukn_bone3;
    //if (BoneNameOffset != 0) {
    char Name[] @ BoneNameOffset;
    //}
}[[name(std::format("{}", Name))]];

struct VMP{
Header HDR;
boneInfo Bones[HDR.BoneCount] @ HDR.BoneOffset;
};

VMP model @ 0;