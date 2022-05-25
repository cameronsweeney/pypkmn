import rby.index, tools
import copy

def move_header_offset(rippening, index):
    return 0x038000 + 6*(index-1) # source: https://datacrystal.romhacking.net/wiki/Pokémon_Red_and_Blue:ROM_map#Bank_E

def parse_move_bytes(bytes, offset):
    return {
        'id': bytes[0],
        'name': rby.index.moves[bytes[0]],
        'effect': rby.index.move_effects[bytes[1]],
        'power': bytes[2],
        'type': rby.index.types[bytes[3]],
        'accuracy': bytes[4],
        'pp': bytes[5]
    }

