## rby/tools.py
import yaml
from . import pokedex, index

offsets = {
    'pkmn_species': {
        ## source: https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_species_data_structure_(Generation_I)
        'red': 0x0383DE,
        'blue': 0x0383DE,
        'yellow': 0x0383DE
    },

    'mew_species': {
        ## source: https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_species_data_structure_(Generation_I)
        'red': 0x00425B, # in RB, Mew's species header is in a weird place
        'blue': 0x00425B,
        'yellow': 0x39446 # located right after Mewtwo's data
    },

    'evo_learnset': {
        'red': 0x03B05C, # source: https://datacrystal.romhacking.net/wiki/Pok%C3%A9mon_Red_and_Blue:ROM_map#Bank_E
        'blue': 0x03B05C,
        'yellow': 0x03B1E5 # source: http://aurellem.org/vba-clojure/html/rom.html#sec-9-1
    },

    'moves': {
        ## source: https://datacrystal.romhacking.net/wiki/Pokémon_Red_and_Blue:ROM_map#Bank_E
        'red': 0x38000,
        'blue': 0x38000,
        'yellow': 0x38000
    }

}


def make_pkmn(natdex):
    name = pokedex.natdex[natdex]
    name_url = pokedex.natdex_url[natdex]
    return {
        'natdex': natdex,
        'name': name,
        'name_url': name_url
    }

def make_evolution(pkmn, into, how, when):
    return {
        'pkmn': pkmn,
        'into': into,
        'how': how,
        'when': when
    }

def parse_pkmn_bytes(bytes):
    
    natdex = bytes[0]

    # find RBY internal index number for Pokemon
    current_pkmn_name = pokedex.natdex[natdex]
    current_pkmn_index = list(index.pkmn.keys())[list(index.pkmn.values()).index(current_pkmn_name)]
    
    return {
        'natdex': natdex,
        'pkmn': current_pkmn_name,
        'id': current_pkmn_index,

        'hp': bytes[1],
        'attack': bytes[2],
        'defense': bytes[3],
        'speed': bytes[4],
        'special': bytes[5],

        'type1': index.types[bytes[6]],
        'type2': index.types[bytes[7]],

        'catch_rate': bytes[8],
        'base_exp': bytes[9],

        'growth_rate': index.growth_rates[bytes[0x13]],
        'tmhm_bits': bytes[0x14:0x1B],

        'learnbase': [
            index.moves[bytes[15]],
            index.moves[bytes[16]],
            index.moves[bytes[17]],
            index.moves[bytes[18]]
        ]
    }

def get_learnbases_only(pkmn_as_yaml):
    # this function accepts a list of YAML objects created by parse_pkmn_bytes above
    # and returns a list of YAML objects of moves found in each Pokémon's 'learnbase' key
    basemove_list = []
    for current_pkmn in pkmn_as_yaml:
        current_obj = yaml.safe_load(current_pkmn)
        current_learnbase = current_obj['learnbase']
        for move in current_learnbase:
            if not move:
                continue
            else:
                new_move = {
                    'pkmn': current_obj['pkmn'],
                    'move': move,
                    'level': 0
                }
                basemove_list.append(yaml.safe_dump(new_move))
    return basemove_list

def parse_evolution_learnset(pkmn, bytes):
    evolutions = []
    learnset = []
    current_byte = 0
    length = len(bytes)
    evo_mode = True

    while current_byte < length:
        if evo_mode: # parse evolutions
            evo_type = bytes[current_byte]
            if evo_type == 0: # end of evolutions
                if current_byte == 0: # there were no evolutions
                    evolutions.append(None)
                current_byte += 1
                evo_mode = False
                continue
            elif evo_type == 1: # level-up, 3 bytes
                level = bytes[current_byte+1]
                into = bytes[current_byte+2]
                current_evo = make_evolution(pkmn, index.pkmn[into], 'Level-up', level)
                evolutions.append(current_evo)
                current_byte += 3
            elif evo_type == 2: # item, 4 bytes
                item = bytes[current_byte+1]
                into = bytes[current_byte+3]
                current_evo = make_evolution(pkmn, index.pkmn[into], index.items[item], 0)
                evolutions.append(current_evo)
                current_byte += 4
            elif evo_type == 3: # trade, 3 bytes
                into = bytes[current_byte+2]
                current_evo = make_evolution(pkmn, index.pkmn[into], 'Trade', 0)
                evolutions.append(current_evo)
                current_byte += 3
        else: # evo_mode is false; now to parse learnset
            level = bytes[current_byte]
            if level:
                move = bytes[current_byte+1]
                learnset.append([index.moves[move], level])
                current_byte += 2
            else: # end of learnset
                current_byte += 1
    
    learnset_dict = {
        'name': pkmn,
        'moves': learnset
    }

    return (evolutions, learnset_dict)

def parse_move_bytes(name, bytes):
    return {
        'name': name,
        'id': bytes[0],
        'effect': index.move_effects[bytes[1]],
        'power': bytes[2],
        'type': index.types[bytes[3]],
        'accuracy': bytes[4],
        'pp': bytes[5]
    }

## this function resolves a local pointer, given bank # and pointer #
def resolve_offset(bank, pointer_as_2_bytes):
    # first convert pointer to big endian
    pointer = pointer_as_2_bytes[0] + (0x100 * pointer_as_2_bytes[1])
    # pointer is in [0x4000, 0x7FFF] - interpret as value in [0x000, 0x3FFF]
    pointer -= 0x4000
    return pointer + (0x4000 * bank)

## source for understanding GB/C pointers: https://hax.iimarckus.org/topic/1627/
## a pointer between 0x4000 and 0x7FFF inclusive points to the ROM's current bank (length 0x4000)
## pointers in [0x0000, 0x3FFF], [0x8000, 0xBFFF], etc. have own meanings for ROM/RAM banks

def bcd_decode(bytes):
    # input is the raw bytes from the ROM representing a binary-coded decimal number
    # output is a Python integer of the encoded value
    result = 0
    for byte in bytes:
        result *= 100
        result += 10*(byte // 16) + byte % 16
    return result