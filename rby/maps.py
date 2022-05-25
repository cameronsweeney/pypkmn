import copy
from re import X

import tools
import rby.index

def parse_connection(bytes):
    if not bytes:
        return None
    else:
        return copy.copy({
            'index': bytes[0],
            'pointer_to_map_start': bytes[1:3].hex().upper(),
            'pointer_to_connection_start': bytes[3:5].hex().upper(),
            'connection_size': bytes[5],
            'connection_width': bytes[6],
            'offset_x': bytes[7],
            'offset_y': bytes[8],
            'pointer_to_window': bytes[9:11].hex().upper(),
        })

def read_map_connection_bytes(rippening, offset):    
    byte = rippening['romdump'][offset]
    count = 0
    for x in range(0, 4):
        if (byte & (1<<x)):
            count += 1
    length = 11*count + 1 # plus one because we need to rip the connections byte, plus 11 bytes for each connection (==11*count)
    connection_bytes = rippening['romdump'][offset:offset+length]
    print(f"{count} connections found, ripping these bytes: {connection_bytes} (length {len(connection_bytes)})")
    return connection_bytes

def map_header_offset(rippening, index):
    # source: https://github.com/pokemon-speedrunning/symfiles
    if rippening['version'] == 'yellow':
        pointer_offset = 0x0FC1F2 + 2*index
        bank_offset = 0x0FC3E4 + index
    else:
        pointer_offset = 0x01AE + 2*index
        bank_offset = 0xC23D + index
    pointer = rippening['romdump'][pointer_offset:pointer_offset+2]
    bank = rippening['romdump'][bank_offset]    
    return tools.resolve_offset(bank, pointer)

def parse_map_header(bytes, offset):
    bank = (offset // 0x4000)
    map_header_dict = {
        'tileset_index': bytes[0],
        'height_in_blocks': bytes[1],
        'width_in_blocks': bytes[2],
        'pointer_to_map_bytes': f"0x{tools.resolve_offset(bank, bytes[3:5]):X}",
        'pointer_to_text_scripts_bytes': f"0x{tools.resolve_offset(bank, bytes[5:7]):X}",
        'pointer_to_map_scripts_bytes': f"0x{tools.resolve_offset(bank, bytes[7:9]):X}",
        'connections': {},
        'map_object_pointer_bytes': '0x' + bytes[-2:].hex().upper(),
        'map_objects': tools.resolve_offset(bank, bytes[-2:])
        #tools.resolve_extremely_local_pointer(bank_100, bytes[-2:]) 
    }
    

    if map_header_dict['map_objects'] == 0x1CB0A:
        map_header_dict['map_objects'] += 0x900
    elif map_header_dict['map_objects'] == 0x748DE:
        map_header_dict['map_objects'] += 0x300
    elif map_header_dict['map_objects'] == 0x5C0C1:
        map_header_dict['map_objects'] += 0x200
    elif map_header_dict['map_objects'] == 0x1DE07 or map_header_dict['map_objects'] == 0x5D520:
        map_header_dict['map_objects'] += 0x100

    map_header_dict['map_objects_hex'] = f"0x{map_header_dict['map_objects']:X}"

    byte = bytes[9] # this byte has connection data
    connection_bytes = copy.deepcopy(bytes[10:-2])
    
    directions = ['east', 'west', 'south', 'north']
    if byte:
        for x in [0, 1, 2, 3]:
            if byte & (1<<x):
                map_header_dict['connections'][directions[x]] = parse_connection(connection_bytes[0:11])
                del connection_bytes[0:11]

    return map_header_dict 

def parse_warp_data(arg_bytes):
    warp_data = []
    my_bytes = copy.deepcopy(arg_bytes)
    while my_bytes:
        warp_data.append({
            'x': my_bytes[0],
            'y': my_bytes[1],
            'warp_in_index': my_bytes[2],
            'target_map': my_bytes[3]
        })
        del my_bytes[0:4]
    return warp_data

def parse_sign_data(arg_bytes):
    sign_data = []
    my_bytes = copy.deepcopy(arg_bytes)
    while my_bytes:
        sign_data.append({
            'x': my_bytes[0],
            'y': my_bytes[1],
            'text_script_index': my_bytes[2]
        })
        del my_bytes[0:3]
    return sign_data

def parse_warp_in_data(my_bytes):
    warp_in_data = []
    while my_bytes:
        warp_in_data.append({
            'pointer_to_window': my_bytes[0],
            'x': my_bytes[1],
            'y': my_bytes[2]
        })
        del my_bytes[0:3]
    return warp_in_data

def parse_map_object(rippening, offset):
    length = 1
    map_object_dict = {
        'border_blocks': rippening['romdump'][offset],
        'warp_count': rippening['romdump'][offset+1],
        'sprites': []
    }
    
    if map_object_dict['warp_count']:
        length = 2+4*map_object_dict['warp_count']
        warp_bytes = bytearray(list(rippening['romdump'][offset+2:offset+length]))
        map_object_dict['warps'] = parse_warp_data(warp_bytes)
    else:
        length = 2

    running_offset = offset + length
    map_object_dict['sign_count'] = rippening['romdump'][running_offset]
    if map_object_dict['sign_count']:
        length = 1+3*map_object_dict['sign_count']
        sign_bytes = bytearray(list(rippening['romdump'][running_offset+1:running_offset+length]))
        map_object_dict['signs'] = parse_sign_data(sign_bytes)
    else:
        length = 1

    running_offset += length
    map_object_dict['sprite_count'] = rippening['romdump'][running_offset]
    running_offset += 1
    for sprite in range(0, map_object_dict['sprite_count']):
        my_bytes = bytearray(rippening['romdump'][running_offset:running_offset+6])
        sprite_dict = {
            'sprite_index': my_bytes[0],
            'x': my_bytes[1]-4,
            'y': my_bytes[2]-4,
            'mobility': my_bytes[3],
            'movement_pattern': my_bytes[4],
            'text_script_index': my_bytes[5]%64
        }
        type_byte = my_bytes[5]
        if type_byte & (1<<6):
            # battle sprite
            my_bytes.append(rippening['romdump'][running_offset+6])
            my_bytes.append(rippening['romdump'][running_offset+7])
            running_offset += 8
            if my_bytes[6] < 0xC8: # interpret as wild Pokémon
                sprite_dict['wild_pkmn'] = rby.index.pkmn[my_bytes[6]]
                sprite_dict['wild_level'] = my_bytes[7]
            else: # interpret as trainer battle
                sprite_dict['trainer_class'] = my_bytes[6] - 0xC8
                sprite_dict['trainer_team'] = my_bytes[7]
        elif type_byte & (1<<7):
            # item sprite
            my_bytes.append(rippening['romdump'][running_offset+6])
            if my_bytes[6]:
                sprite_dict['item'] = rby.index.items[my_bytes[6]]
            running_offset += 7
        else:
            running_offset += 6
        map_object_dict['sprites'].append(sprite_dict)
    
    if map_object_dict['warp_count']:
        length = 3*map_object_dict['warp_count']
        warp_in_bytes = bytearray(list(rippening['romdump'][running_offset:running_offset+length]))
        map_object_dict['warp_in_data'] = parse_warp_in_data(warp_in_bytes)
    
    map_object_dict['binary'] = rippening['romdump'][offset:running_offset+length].hex().upper()

    return map_object_dict


def trainer_teams_offset(rippening, index):
    if rippening['version'] == 'yellow':
        pointer_offset = 0x39DD1 + 2*(index-1)
    else:
        pointer_offset = 0x39D3B + 2*(index-1)
    pointer_value = tools.resolve_offset(0xE, rippening['romdump'][pointer_offset:pointer_offset+2])
    if index != 0x2F:
        next_pointer_value = tools.resolve_offset(0xE, rippening['romdump'][pointer_offset+2:pointer_offset+4])
    else: # Lance, last trainer class - need to give length & not interpret next word as another pointer
        next_pointer_value = pointer_value + 12
    print(f'Offset 0x{pointer_offset:X} points to 0x{pointer_value:X}')
    return (pointer_value, next_pointer_value)

def parse_trainer_teams(bytes, offset):
    # source for explanation of teams' data structure: https://github.com/pret/pokered/blob/master/data/trainers/parties.asm
    teams = {}
    current_team = []
    team_count = 1
    x = 0
    print(bytes.hex().upper())
    print(f'0x{offset[0]:X}')

    while x < len(bytes):
        if bytes[x] == 0xFF:
            x += 1
            while (x<len(bytes)) and bytes[x]:
                level = bytes[x]
                pkmn = rby.index.pkmn[bytes[x+1]]
                current_team.append(f"{pkmn} Lv.{level}")
                x += 2
        else:
            level = bytes[x]
            x += 1
            while (x<len(bytes)) and bytes[x]:
                pkmn = rby.index.pkmn[bytes[x]]
                current_team.append(f"{pkmn} Lv.{level}")
                x += 1
        teams[team_count] = copy.deepcopy(current_team)
        team_count += 1
        current_team = []
        x += 1

    print(teams)
    return {'teams': teams}

def wild_encounters_offset(rippening, index):
    if rippening['version'] == 'yellow':
        pointer_offset = 0xCB95 + 2*(index)
    else:
        pointer_offset = 0xCEEB + 2*(index)
    print(f"Reading pointer at 0x{pointer_offset:X}...")
    return tools.resolve_offset(0x3, rippening['romdump'][pointer_offset:pointer_offset+2])

def parse_wild_encounters(bytes, offset):
    # source: https://github.com/pret/pokered/blob/master/data/wild/grass_water.asm
    print(f"Following pointer to 0x{offset:X}...")
    encounters_dict = {
        'grass_rate': bytes[0]
    }
    if encounters_dict['grass_rate']:
        grass_encounters = []
        for x in range(0,10):
            level = bytes[1+2*x]
            pkmn = rby.index.pkmn[bytes[2+2*x]]
            string = f"{pkmn} Lv.{level}"
            print(string)
            grass_encounters.append(string)
        grass_length = 21
        encounters_dict['grass'] = grass_encounters
    else:
        grass_length = 1
    
    encounters_dict['surf_rate'] = bytes[grass_length]
    if encounters_dict['surf_rate']:
        surf_encounters = []
        for x in range(0, 10):
            level = bytes[1+2*x+grass_length]
            pkmn = rby.index.pkmn[bytes[2+2*x+grass_length]]
            surf_encounters.append(f"{pkmn} Lv.{level}")
        encounters_dict['surf'] = surf_encounters
    
    return encounters_dict

rb_fish_groups_by_map = {
    ## In Red and Blue, each map has a fishing group (0 if there's no water)
    ## This fishing group determines the map's Super Rod encounters
    ## In Yellow, the fishable maps each have their own Super Rod encounter tables, so this data is RB only.
    
    ## Source: https://aww.moe/u408xw.asm => "SuperRodData: ; e919 (3:6919)"
    ## snapshot at https://web.archive.org/web/20200822125414/https://aww.moe/u408xw.asm

    0x00: 1, # Pallet Town
    0x01: 1, # Viridian City
    0x03: 3, # Cerulean City
    0x05: 4, # Vermilion City
    0x06: 5, # Celadon City
    0x07: 10, # Fuchsia City
    0x08: 8, # Cinnabar Island
    0x0F: 3, # Route 4
    0x11: 4, # Route 6
    0x15: 5, # Route 10
    0x16: 4, # Route 11
    0x17: 7, # Route 12
    0x18: 7, # Route 13
    0x1C: 7, # Route 17
    0x1D: 7, # Route 18
    0x1E: 8, # Route 19
    0x1F: 8, # Route 20
    0x20: 8, # Route 21
    0x21: 2, # Route 22
    0x22: 9, # Route 23
    0x23: 3, # Route 24
    0x24: 3, # Route 25
    0x41: 3, # Cerulean Gym
    0x5E: 4, # Vermilion Dock
    0xA1: 8, # Seafoam Islands B3
    0xA2: 8, # Seafoam Islands B4
    0xD9: 6, # Safari Zone East
    0xDA: 6, # Safari Zone North
    0xDB: 6, # Safari Zone West
    0xDC: 6, # Safari Zone Center
#   0xE2: 9, # Cerulean Cave 2F - no water to fish in here!
    0xE3: 9, # Cerulean Cave B1
    0xE4: 9 # Cerulean Cave 1F
}

rby_fish_encounters_as_yaml = """
## Every map in RBY has the same Old Rod & Good Rod encounters
## Sources:
## https://sites.google.com/site/pokemonslots/gen-i/red
## https://github.com/pret/pokered/blob/master/data/wild/good_rod.asm
## https://aww.moe/u408xw.asm => "ItemUseOldRod: ; e24c (3:624c)"
## snapshot at https://web.archive.org/web/20200822125414/https://aww.moe/u408xw.asm
old_rod:
  - [Magikarp Lv.5]

good_rod:
  - [Goldeen Lv.10, Poliwag Lv.10]


super_rod:
  rb:
  ## in Red/Blue, each fishable map has a fishing group that determines the encounter table
  ## RB Super Rod source: https://github.com/pret/pokered/blob/master/data/wild/super_rod.asm
  ## see also https://aww.moe/u408xw.asm => "FishingGroup1: ; e97d (3:697d)"
    - [] # fish group 0 means no water to fish in
    - [Tentacool Lv.15, Poliwag Lv.15] # Fish Group 1; this list is one-indexed
    - [Goldeen Lv.15, Poliwag Lv.15]
    - [Psyduck Lv.15, Goldeen Lv.15, Krabby Lv.15]
    - [Krabby Lv.15, Shellder Lv.15]
    - [Poliwhirl Lv.23, Slowpoke Lv.15]
    - [Dratini Lv.15, Krabby Lv.15, Psyduck Lv.15, Slowpoke Lv.15]
    - [Tentacool Lv.5, Krabby Lv.15, Goldeen Lv.15, Magikarp Lv.15]
    - [Staryu Lv.15, Horsea Lv.15, Shellder Lv.15, Goldeen Lv.15]
    - [Slowbro Lv.23, Seaking Lv.23, Kingler Lv.23, Seadra Lv.23]
    - [Seaking Lv.23, Krabby Lv.15, Goldeen Lv.15, Magikarp Lv.15]

  y:
  ## in Yellow, each fishable map has its own encounter table
  ## Yellow Super Rod source: https://github.com/pret/pokeyellow/blob/master/data/wild/super_rod.asm
    0x00: [Staryu Lv.10, Tentacool Lv.10, Staryu Lv.5, Tentacool Lv.20]       # Pallet Town
    0x01: [Poliwag Lv.5, Poliwag Lv.10, Poliwag Lv.15, Poliwag Lv.10]         # Viridian City
    0x03: [Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30, Seaking Lv.40]        # Cerulean City
    0x05: [Tentacool Lv.15, Tentacool Lv.20, Tentacool Lv.10, Horsea Lv.5]    # Vermilion City
    0x06: [Goldeen Lv.5, Goldeen Lv.10, Goldeen Lv.15, Goldeen Lv.20]         # Celadon City
    0x07: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Gyarados Lv.15]     # Fuchsia City
    0x08: [Staryu Lv.15, Tentacool Lv.15, Staryu Lv.10, Tentacool Lv.30]      # Cinnabar Island
    0x0F: [Goldeen Lv.20, Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30]        # Route 4
    0x11: [Goldeen Lv.5, Goldeen Lv.10, Goldeen Lv.15, Goldeen Lv.20]         # Route 6
    0x15: [Krabby Lv.15, Krabby Lv.20, Horsea Lv.10, Kingler Lv.25]           # Route 10
    0x16: [Tentacool Lv.15, Tentacool Lv.20, Shellder Lv.25, Shellder Lv.35]  # Route 11
    0x17: [Horsea Lv.20, Horsea Lv.25, Seadra Lv.25, Seadra Lv.35]            # Route 12
    0x18: [Horsea Lv.15, Horsea Lv.20, Seadra Lv.25, Seadra Lv.25]            # Route 13
    0x1C: [Tentacool Lv.5, Tentacool Lv.15, Shellder Lv.25, Shellder Lv.35]   # Route 17
    0x1D: [Tentacool Lv.15, Shellder Lv.20, Shellder Lv.30, Shellder Lv.40]   # Route 18
    0x1E: [Tentacool Lv.15, Staryu Lv.20, Tentacool Lv.30, Tentacruel Lv.30]  # Route 19
    0x1F: [Tentacool Lv.20, Tentacruel Lv.20, Staryu Lv.30, Tentacruel Lv.30] # Route 20
    0x20: [Tentacool Lv.15, Staryu Lv.20, Tentacool Lv.30, Tentacruel Lv.30]  # Route 21
    0x21: [Poliwag Lv.5, Poliwag Lv.10, Poliwag Lv.15, Poliwhirl Lv.15]       # Route 22
    0x22: [Poliwag Lv.25, Poliwag Lv.30, Poliwhril Lv.30, Poliwhirl Lv.40]    # Route 23
    0x23: [Goldeen Lv.20, Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30]        # Route 24
    0x24: [Krabby Lv.10, Krabby Lv.15, Kingler Lv.15, Kingler Lv.25]          # Route 25
    0x41: [Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30, Seaking Lv.40]        # Cerulean Gym
    0x5E: [Tentacool Lv.10, Tentacool Lv.15, Staryu Lv.15, Shellder Lv.10]    # Vermilion Dock
    0xA1: [Krabby Lv.25, Staryu Lv.20, Kingler Lv.35, Staryu Lv.40]           # Seafoam Islands B3
    0xA2: [Krabby Lv.25, Staryu Lv.20, Kingler Lv.35, Staryu Lv.40]           # Seaforam Islands B4
    0xD9: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Dratini Lv.15]      # Safari Zone East
    0xDA: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Dratini Lv.15]      # Safari Zone North
    0xDB: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Dratini Lv.15]      # Safari Zone West
    0xDC: [Magikarp Lv.5, Magikarp Lv.10, Dratini Lv.10, Dragonair Lv.15]     # Safari Zone Center
    0xE3: [Goldeen Lv.30, Seaking Lv.40, Seaking Lv.50, Seaking Lv.60]        # Cerulean Cave B1
    0xE4: [Goldeen Lv.25, Seaking Lv.35, Seaking Lv.45, Seaking Lv.55]        # Cerulean Cave 1F
"""


    