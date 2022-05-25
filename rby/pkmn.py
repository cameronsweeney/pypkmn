import copy

import rby.index
import tools

def pkmn_header_offset(rippening, index):
    if index == 151 and rippening['version'] != 'yellow':
        return 0x425B
    else:
        return 0x0383DE + 28*(index-1)

def parse_pkmn_header(bytes, offset):
    natdex = bytes[0]
    name = rby.index.natdex[natdex]
    index = list(rby.index.pkmn.keys())[list(rby.index.pkmn.values()).index(name)]
    return {
        'natdex': bytes[0],
        'name': rby.index.natdex[bytes[0]],
        'index': index,

        'hp': bytes[1],
        'attack': bytes[2],
        'defense': bytes[3],
        'speed': bytes[4],
        'special': bytes[5],

        'type1': rby.index.types[bytes[6]],
        'type2': rby.index.types[bytes[7]],

        'catch_rate': bytes[8],
        'base_exp': bytes[9],

        'growth_rate': rby.index.growth_rates[bytes[0x13]],
        'tmhm_bits': bytes[0x14:0x1B].hex(),

        'learnbase': [
            rby.index.moves[bytes[15]],
            rby.index.moves[bytes[16]],
            rby.index.moves[bytes[17]],
            rby.index.moves[bytes[18]]
        ]
    }

def evolutions_levelups_offset(rippening, index):
    if rippening['version'] == 'yellow':
        offset = 0x03B1E5 # source: http://aurellem.org/vba-clojure/html/rom.html#sec-9-1
    else:
        offset = 0x03B05C
    pointer_offset = offset + 2*(index-1)
    pointer_bytes = rippening['romdump'][pointer_offset:pointer_offset+2]
    resolved_offset = tools.resolve_offset(0xE, pointer_bytes)
    return resolved_offset

def parse_evolution_levelup(bytes, offset):
    evolutions = []
    levelups = []
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
            elif evo_type == 1: # level-up, 3 bytes
                level = bytes[current_byte+1]
                into = bytes[current_byte+2]
                current_evo = {'into': rby.index.pkmn[into], 'how': 'Level-up', 'when': level}
                evolutions.append(current_evo)
                current_byte += 3
            elif evo_type == 2: # item, 4 bytes
                item = bytes[current_byte+1]
                into = bytes[current_byte+3]
                current_evo = {'into': rby.index.pkmn[into], 'how': 'Item', 'with': rby.index.items[item]}
                evolutions.append(current_evo)
                current_byte += 4
            elif evo_type == 3: # trade, 3 bytes
                into = bytes[current_byte+2]
                current_evo = {'into': rby.index.pkmn[into], 'how': 'Trade'}
                evolutions.append(current_evo)
                current_byte += 3
        else: # evo_mode is false; now to parse level-up moves
            level = bytes[current_byte]
            if level:
                move = bytes[current_byte+1]
                levelups.append({'move': rby.index.moves[move], 'level': level})
                current_byte += 2
            else: # end of level-up moves
                current_byte += 1
    
    return {'evolutions': copy.copy(evolutions), 'levelups': copy.copy(levelups)}

def pokedex_offset(rippening, index):
    if rippening['version'] == 'yellow':
        offset = 0x04050B 
        ## found offset myself, based on info from aurellem.org/vba-clojure/html/rom.html
        ## starting at 0x040687 is Bulbasaur's data, ends at 2nd 0x50 byte
        ## determined Ivysaur's offset was 0x40695 -> search rom for bytes 9546
        ## there were 2 instances at offsets 0x4051B and 0xE4607; confirmed by following adjacent pointers
        ## Ivysaur is index 9 -> subtract 0x8*0x2=0x10 bytes to get Rhydon's pointer (index 1)
    else:
        offset = 0x04047E # source: https://www.smogon.com/smog/issue27/glitch
    pointer_offset = offset + 2*(index-1)
    pointer_bytes = rippening['romdump'][pointer_offset:pointer_offset+2]
    resolved_offset = tools.resolve_offset(0x10, pointer_bytes)
    return resolved_offset

def parse_pokedex(bytes):
    # source: https://www.smogon.com/smog/issue27/glitch
    species_name_length = bytes.index(0x50)
    return {
        'species_name': tools.decode_rby_text(bytes[0:species_name_length]),
        'height_ft': bytes[species_name_length+1],
        'height_in': bytes[species_name_length+2],
        'weight': (bytes[species_name_length+3] + 0x100*bytes[species_name_length+4])/10,
        'pokedex_text': tools.resolve_offset(bytes[species_name_length+8], bytes[species_name_length+6:species_name_length+8])
    }

