char[] magic_string = { 0x56, 0x65, 0x72, 0x73, 0x69, 0x6f, 0x6e, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
void setupKeys(void)

{
  DAT_01817e30 = 0xeb7d;
  DAT_01817e32 = 0xa2f1;
  DAT_01817e34 = 7;
  FUN_018056a4(0x1817e36,magic_string);
  DAT_01817e40 = 0xebd7;
  DAT_01817e42 = 0xa21f;
  DAT_01817e44 = 0xd;
  FUN_018056a4(0x1817e46,magic_string);
}
void FUN_018056a4(ulong *param_1,char magic_str[16])

{
  char cVar1;
  ulong uVar2;
  undefined auVar3 [16];
  undefined8 in_a0_udw;
  undefined auVar4 [16];
  undefined (*pauVar5) [16];
  undefined auVar6 [16];
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 in_t1_udw;
  undefined4 uVar9;
  undefined4 in_register_0000009c;
  undefined4 uVar10;
  ulong uVar11;
  undefined auVar12 [16];
  
  if ((((uint)param_2 | (uint)param_1) & 7) == 0) {
    auVar3._8_8_ = in_a0_udw;
    auVar3._0_8_ = 0x8080808080808080;
    if ((((uint)param_2 | (uint)param_1) & 0xf) == 0) {
      auVar4._8_4_ = in_t1_udw;
      auVar4._0_8_ = 0x101010101010101;
      auVar4._12_4_ = in_register_0000009c;
      auVar6._8_4_ = in_t1_udw;
      auVar6._0_8_ = 0x101010101010101;
      auVar6._12_4_ = in_register_0000009c;
      auVar12 = _pcpyld(auVar4,auVar6);
      uVar7 = *(undefined4 *)*param_2;
      uVar8 = *(undefined4 *)(*param_2 + 4);
      uVar9 = *(undefined4 *)(*param_2 + 8);
      uVar10 = *(undefined4 *)(*param_2 + 0xc);
      auVar6 = _pcpyld(auVar3,auVar3);
      auVar3 = _psubb(*param_2,auVar12);
      auVar3 = _pand(auVar3,~*param_2);
      auVar3 = _pand(auVar3,auVar6);
      auVar4 = _pcpyud(auVar3,*param_2);
      uVar11 = auVar3._0_8_ | auVar4._0_8_;
      while (uVar11 == 0) {
        *(undefined4 *)param_1 = uVar7;
        *(undefined4 *)((int)param_1 + 4) = uVar8;
        *(undefined4 *)(param_1 + 1) = uVar9;
        *(undefined4 *)((int)param_1 + 0xc) = uVar10;
        pauVar5 = param_2 + 1;
        uVar7 = *(undefined4 *)*pauVar5;
        uVar8 = *(undefined4 *)(param_2[1] + 4);
        uVar9 = *(undefined4 *)(param_2[1] + 8);
        uVar10 = *(undefined4 *)(param_2[1] + 0xc);
        auVar3 = _psubb(*pauVar5,auVar12);
        auVar3 = _pand(auVar3,~*pauVar5);
        auVar3 = _pand(auVar3,auVar6);
        auVar4 = _pcpyud(auVar3,*pauVar5);
        param_1 = param_1 + 2;
        param_2 = pauVar5;
        uVar11 = auVar3._0_8_ | auVar4._0_8_;
      }
    }
    else {
      uVar11 = *(ulong *)*param_2;
      uVar2 = uVar11 + 0xfefefefefefefeff & ~uVar11;
      while ((uVar2 & 0x8080808080808080) == 0) {
        *param_1 = uVar11;
        param_2 = (undefined (*) [16])(*param_2 + 8);
        uVar11 = *(ulong *)*param_2;
        param_1 = param_1 + 1;
        uVar2 = uVar11 + 0xfefefefefefefeff & ~uVar11;
      }
    }
  }
  do {
    cVar1 = (*param_2)[0];
    param_2 = (undefined (*) [16])(*param_2 + 1);
    *(char *)param_1 = cVar1;
    param_1 = (ulong *)((int)param_1 + 1);
  } while (cVar1 != '\0');
  return;
}

bool Decrypter(ushort *key_store,byte *output_buffer,byte *input_buffer,int bufsize)

{
  bool bVar1;
  uint uVar2;
  ulong magicXor_Key1;
  ulong xored_back_front;
  ushort *key_store_next;
  int current_pointer;
  ulong xored_result;
  int backward_pointer;
  ulong magicXor_Key2;
  uint cur_value_input;
  byte *cur_input_point;
  byte first_byte;
  ushort magicXor_Key3;
  
  current_pointer = bufsize + -0xb;
  magicXor_Key1 = (ulong)*key_store;
  cur_value_input = (uint)*(ushort *)(input_buffer + current_pointer);
  magicXor_Key2 = (ulong)key_store[1];
  xored_result = magicXor_Key1 ^
                 (long)(int)((uint)(*(ushort *)(input_buffer + current_pointer) >> 3) |
                            cur_value_input << 0xd) & 0xffffU;
  cur_input_point = input_buffer;
  if (current_pointer < 1) {
    magicXor_Key1 = (ulong)*key_store;
    first_byte = *input_buffer;
  }
  else {
    magicXor_Key3 = key_store[2];
    backward_pointer = current_pointer;
    do {
      xored_back_front = *cur_input_point ^ xored_result;
      xored_result = (long)(int)(((uint)xored_result >> 1 | ((uint)xored_result & 1) << 0xf) * 5 + 1
                                ) & 0xffff;
      cur_input_point = cur_input_point + 1;
      uVar2 = FUN_01803418(xored_back_front & 0xff,magicXor_Key3);
      backward_pointer = backward_pointer + -1;
      magicXor_Key2 = (long)(int)((int)magicXor_Key2 + (uVar2 & 0xffff)) & 0xffff;
    } while (0 < backward_pointer);
    first_byte = *cur_input_point;
  }
  magicXor_Key1 =
       ((ulong)(ushort)(CONCAT11(cur_input_point[1],first_byte) >> 3) |
       ((ulong)CONCAT11(cur_input_point[1],first_byte) & 7) << 0xd) ^ magicXor_Key1;
  cur_input_point = cur_input_point + 2;
  if (magicXor_Key1 == magicXor_Key2) {
    key_store_next = key_store + 3;
    do {
      first_byte = *(byte *)key_store_next;
      uVar2 = *cur_input_point ^ cur_value_input;
      key_store_next = (ushort *)((int)key_store_next + 1);
      cur_input_point = cur_input_point + 1;
      cur_value_input = (cur_value_input >> 5 | (cur_value_input & 0x1f) << 0xb) * 5 + 1 & 0xffff;
      if ((uVar2 & 0xff) != (uint)first_byte) goto LAB_018011b8;
    } while (*(byte *)key_store_next != 0);
    for (; 0 < current_pointer; current_pointer = current_pointer + -1) {
      *output_buffer = *input_buffer ^ (byte)magicXor_Key1;
      magicXor_Key1 =
           (long)(int)(((uint)magicXor_Key1 >> 1 | ((uint)magicXor_Key1 & 1) << 0xf) * 5 + 1) &
           0xffff;
      input_buffer = input_buffer + 1;
      output_buffer = output_buffer + 1;
    }
    bVar1 = false;
  }
  else {
LAB_018011b8:
    bVar1 = true;
  }
  return bVar1;
}

ulong FUN_01803418(ulong param_1,ulong param_2)

{
  ulong uVar1;
  
  uVar1 = (param_1 & 0xffffffff) * (param_2 & 0xffffffff);
  return uVar1 & 0xffffffff |
         (long)((int)(uVar1 >> 0x20) +
               (int)param_1 * (int)(param_2 >> 0x20) + (int)(param_1 >> 0x20) * (int)param_2) <<
         0x20;
}

