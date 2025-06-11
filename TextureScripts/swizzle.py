from cffi import FFI
ffi = FFI()

ffi.set_source("_get_swizzled_offset", """
static uint32_t fill_pattern(uint32_t pattern, uint32_t value)
{
    uint32_t result = 0;
    uint32_t bit = 1;
    while(value) {
        if (pattern & bit) {
            /* Copy bit to result */
            result |= value & 1 ? bit : 0;
            value >>= 1;
        }
        bit <<= 1;
    }
    return result;
}

static unsigned int get_swizzled_offset(
    unsigned int x, unsigned int y, unsigned int z,
    uint32_t mask_x, uint32_t mask_y, uint32_t mask_z,
    unsigned int bytes_per_pixel)
{
    return bytes_per_pixel * (fill_pattern(mask_x, x)
                           | fill_pattern(mask_y, y)
                           | fill_pattern(mask_z, z));
}
""")

ffi.cdef("""int get_swizzled_offset(unsigned int, unsigned int, unsigned int,
    uint32_t, uint32_t, uint32_t,
    unsigned int);""")
ffi.compile()
from _get_swizzled_offset import lib as getSwizzed

ffi1 = FFI()

ffi1.set_source("_generate_swizzle_masks", """
     int * generate_swizzle_masks(unsigned int width,
                                   unsigned int height,
                                   unsigned int depth)
{
    uint32_t x = 0, y = 0, z = 0;
    int * ret = (int *) malloc(sizeof(int)*3);
    uint32_t bit = 1;
    uint32_t mask_bit = 1;
    int done = 1;
    do {
        done = 1;
        if (bit < width) { x |= mask_bit; mask_bit <<= 1; done = 0; }
        if (bit < height) { y |= mask_bit; mask_bit <<= 1; done = 0; }
        if (bit < depth) { z |= mask_bit; mask_bit <<= 1; done = 0; }
        bit <<= 1;
    } while(!done);
    assert(((x ^ y) ^ z) == (mask_bit - 1));
    ret[0] = x;
    ret[1] = y;
    ret[2] = z;
    return ret;
}
""")

ffi1.cdef("""int *  generate_swizzle_masks(unsigned int, unsigned int, unsigned int);
            void free(void *);""")

ffi1.compile()
from _generate_swizzle_masks import lib as generateSwizz
def c_generate_swizzle_masks(width,height,depth):
    ret = generateSwizz.generate_swizzle_masks(width,height,depth)
    my_python_list = ffi1.unpack(ret, 3)
    generateSwizz.free(ret)
    return my_python_list
    

def generate_swizzle_masks(width,height,depth):
    x=y=z=0
    bit = 1
    mask_bit =1
    while 1:
        done = True
        if (bit < width):
            x |= mask_bit
            mask_bit <<= 1
            done = False
        if (bit < height):
            y |= mask_bit
            mask_bit <<= 1
            done = False
        if (bit < depth):
            z |= mask_bit
            mask_bit <<= 1
            done = False
        if(not done):break
    assert(((x ^ y) ^ z) == (mask_bit - 1))
    return [x,y,z]
def fill_pattern(pattern,value):
    result = 0
    bit = 1
    while(value):
        if (pattern & bit):
            result |= value & 1 if bit else 0
            value >>= 1
        bit <<= 1
    return result
def get_swizzled_offset(x,y,z,mask_x,mask_y,mask_z,bytes_per_pixel):
    return bytes_per_pixel * (fill_pattern(mask_x, x)
                           | fill_pattern(mask_y, y)
                           | fill_pattern(mask_z, z))

def swizzle_box(src_buf,width,height,depth,row_pitch,slice_pitch,bytes_per_pixel):
    mask = c_generate_swizzle_masks(width, height, depth)
    src_off = 0
    dst_buf = bytearray(src_buf)
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                for a in range(bytes_per_pixel):
                    dst_buf[getSwizzed.get_swizzled_offset(x,y,0,mask[0],mask[1],0,bytes_per_pixel)+a] = src_buf[(src_off + y*row_pitch+x*bytes_per_pixel)+a]
        src_off+=slice_pitch
    return dst_buf
def unswizzle_box(src_buf,width,height,depth,row_pitch,slice_pitch,bytes_per_pixel):
    mask = c_generate_swizzle_masks(width, height, depth)
    dst_off = 0
    dst_buf = bytearray(src_buf)
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                for a in range(bytes_per_pixel):
                    dst_buf[(dst_off+y*row_pitch+x*bytes_per_pixel)+a] = src_buf[getSwizzed.get_swizzled_offset(x,y,z,mask[0],mask[1],mask[2],bytes_per_pixel)+a]
        dst_off+=slice_pitch
    return dst_buf
def unswizzle_rect(src_buf,width,height,pitch,bytes_per_pixel):
    return unswizzle_box(src_buf, width, height, 1, pitch, 0, bytes_per_pixel)
def swizzle_rect(src_buf,width,height,pitch,bytes_per_pixel):
    return swizzle_box(src_buf, width, height, 1, pitch, 0, bytes_per_pixel)
