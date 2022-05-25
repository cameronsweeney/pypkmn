import copy, functools
import rby.text_encoding

def bcd_decode(bytes):
    # input is the raw bytes from the ROM representing a binary-coded decimal number
    # output is a Python integer of the encoded value
    result = 0
    for byte in bytes:
        result *= 100
        result += 10*(byte // 16) + byte % 16
    return result

def decode_rby_text(bytes):
    text = ''
    for byte in bytes:
        if byte == 0x50:
            break
        text += rby.text_encoding.charmap[byte]
    return text

def resolve_offset(bank, pointer_as_2_bytes):
    ## this function resolves a local pointer, given bank # and pointer #
    ## source for understanding GB/C pointers: https://hax.iimarckus.org/topic/1627/
    ## a pointer between 0x4000 and 0x7FFF inclusive points to the ROM's current bank (length 0x4000)
    ## pointers in [0x0000, 0x3FFF], [0x8000, 0xBFFF], etc. have own meanings for ROM/RAM banks
    
    # first convert pointer to big endian
    pointer = pointer_as_2_bytes[0] + (0x100 * (pointer_as_2_bytes[1]-0x40))
    return pointer + (0x4000 * bank)


###################################################################

def apply_partial_rip(rip_dict, function):
    if 'bytes' in rip_dict:
        running_bytes = rip_dict['bytes']
    else:
        running_bytes = bytearray()
    new_bytes = function(rip_dict['rip'], rip_dict['offset'])
    length = len(new_bytes)
    running_bytes += new_bytes
    return {**rip_dict, 'bytes': running_bytes, 'offset': rip_dict['offset']+length}

def rip_sequence(*functions):
    return (lambda rip, offset: functools.reduce(apply_partial_rip, functions, {'rip': rip, 'offset': offset})['bytes'])

def read_const_length(length):
    return (lambda rippening, offset: rippening['romdump'][offset:offset+length])

def count_until(rippening, offset, bytes):
    current_offset = offset
    while bytes:
        if rippening['romdump'][current_offset] == bytes[0]:
            del bytes[0]
        current_offset += 1
    return current_offset - offset

def read_until(bytes):
    return (lambda rippening, offset: rippening['romdump'][offset:offset+count_until(rippening, offset, copy.copy(bytes))])

def follow_pointer(structure, points_to):
    return (lambda rippening, index: rippening[structure][index][points_to])

def read_nybble(rippening, offset):
    # if offset is positive, read the high nybble at the offset
    if offset > 0:
        return rippening['romdump'][offset] >> 4
    # if the offset is negative, that means to read the low nybble from that offset (well, from abs(offset))
    else:
        return rippening['romdump'][-offset] % 16

def read_n_const_lengths(length):
    # reads one byte saying how many of a certain (fixed-length) data structure are to follow & rips that byte plus those structures
    return (lambda rippening, offset: rippening['romdump'][offset:offset+(1 + length * rippening['romdump'][offset])] )

# for doing ripping and parsing together - sometimes the logic of parsing & calculating structure length is tied together
# & it's easier to just do it all in one pass - for example with map objects
def pass_offset_to_parser(rippening, offset):
    return rippening

def read_until_next_offset(rippening, offset_tuple):
    # if this function is listed as a data_structure's rip function, its offset function must return a tuple
    # offset_tuple = (offset for current index, offset for next index)
    length = offset_tuple[1] - offset_tuple[0]
    return rippening['romdump'][offset_tuple[0]:offset_tuple[0]+length]
