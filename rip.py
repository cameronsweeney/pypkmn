## rby/rip.py

import yaml
import re
import sys
import os

import rby.tools, rby.meta, rby.index

def rip_pkmn_species_data(romdump, version):
    list_of_pkmn_species_dicts = [''] # not zero-indexed, in national dex order

    # Bulbasaur to Mewtwo
    current_offset = rby.meta.offsets['pkmn_species'][version]
    for current_pkmn in range (1, 151):
        # get bytes from rom & parse them
        raw_bytes = romdump[current_offset:current_offset+28]
        list_of_pkmn_species_dicts.append(rby.tools.parse_pkmn_bytes(raw_bytes))
        current_offset += 28
    
    # Mew
    current_offset = rby.meta.offsets['mew_species'][version]
    raw_bytes = romdump[current_offset:current_offset+28]
    list_of_pkmn_species_dicts.append(rby.tools.parse_pkmn_bytes(raw_bytes))

    return list_of_pkmn_species_dicts

def rip_evolutions_learnsets(romdump, version):
    list_of_evolution_dicts = []
    list_of_learnset_dicts = []
    pointer_table_offset = rby.meta.offsets['evo_learnset'][version]

    for current_index in rby.index.pkmn.keys():
        pkmn_name = rby.index.pkmn[current_index]
        # calculate offset of the nth pointer in the table
        current_pointer_offset = pointer_table_offset + 2*(current_index - 1)
        # read pointer from rom
        current_pointer = [romdump[current_pointer_offset], romdump[current_pointer_offset+1]]
        # resolve pointer, bank 0xE
        resolved_offset = rby.tools.resolve_offset(0xE, current_pointer)
        # read evos_learnset from rom, using calculated offset
        current_byte = resolved_offset
        raw_bytes = []
        zero_byte_count = 0
        while zero_byte_count < 2: # read until second 00 byte
            byte = romdump[current_byte]
            raw_bytes.append(byte)
            if not byte:
                zero_byte_count += 1
            current_byte += 1
        
        # parse bytes into list of (evolution dict) & learnset dict
        (evolutions, learnset) = rby.tools.parse_evolution_learnset(pkmn_name, raw_bytes)
        for evolution in evolutions:
            if evolution:
                list_of_evolution_dicts.append(evolution)
        if learnset:
            list_of_learnset_dicts.append(learnset)

    return (list_of_evolution_dicts, list_of_learnset_dicts)

def rip_move_data(romdump, version):
    list_of_move_dicts = []
    offset_move_data = rby.meta.offsets['moves'][version]
    for current_move_index in rby.index.moves.keys():
        move_name = rby.index.moves[current_move_index]
        # rip move binary data
        current_offset = offset_move_data + 6*(current_move_index - 1)
        raw_bytes = romdump[current_offset:current_offset+6]
        list_of_move_dicts.append(rby.tools.parse_move_bytes(move_name, raw_bytes))
    return list_of_move_dicts

def rip_item_data(romdump, version):
    list_of_item_dicts = []
    for current_item_index in rby.index.items.keys():
        item_name = rby.index.items[current_item_index]
        if current_item_index > 0x53: # is a TM or HM
            if current_item_index < 0xC9: # is an HM
                item_price = 0
            else: # is a TM
                table_offset = rby.meta.offsets['tm_prices'][version]
                tm_number = current_item_index - 0xC8
                price_offset = table_offset + ((tm_number-1) // 2) # tm_number+1 so that (TM02-1)//2 = 0
                price_byte = romdump[price_offset]
                # 2 TM prices stored per byte
                if (tm_number % 2): # odd TM#, need high nybble
                    price_byte >>= 4
                else: # even need low nybble
                    price_byte %= 16
                item_price = price_byte * 1000
        else: # is not a TM/HM
            table_offset = rby.meta.offsets['items'][version]
            price_offset = table_offset + 3*(current_item_index-1)
            raw_bytes = romdump[price_offset:price_offset+3]
            item_price = rby.tools.bcd_decode(raw_bytes)
        item_dict = {
            'name': item_name,
            'id': current_item_index,
            'price': item_price,
        }
        list_of_item_dicts.append(item_dict)
    return list_of_item_dicts


def main(filepath, version, data_flags):
    print(f"Running pypkmn/rip.py on {filepath}, which points to a Pokémon {version.title()} ROM...")
    
    print("Reading ROM contents...")
    romdump = []
    with open(filepath, 'rb') as rom:
        romdump = rom.read()

    if data_flags['pkmn']:
        print(f"Ripping Pokémon species headers to rby/{version}/pkmn.yaml...")
        species_dicts = rip_pkmn_species_data(romdump, version)
        with open(f'rby/{version}/pkmn.yaml', 'w') as out_file:
            out_file.write(yaml.dump_all(species_dicts))

    if data_flags['evolutions']:
        print(f"Ripping evolution and learnset data to rby/{version}/evolutions.yaml and rby/{version}/learnsets.yaml...")
        (evolution_dicts, learnset_dicts) = rip_evolutions_learnsets(romdump, version)
        with open(f'rby/{version}/evolutions.yaml', 'w') as out_file:
            out_file.write(yaml.dump_all(evolution_dicts))
        with open(f'rby/{version}/learnsets.yaml', 'w') as out_file:
            out_file.write(yaml.dump_all(learnset_dicts))

    if data_flags['moves']:
        print(f"Ripping move data to rby/{version}/moves.yaml...")
        move_dicts = rip_move_data(romdump, version)
        with open(f'rby/{version}/moves.yaml', 'w') as out_file:
            out_file.write(yaml.dump_all(move_dicts))

    if data_flags['items']:
        print(f"Ripping item price data to rby/{version}/items.yaml...")
        item_dicts = rip_item_data(romdump, version)
        with open(f'rby/{version}/items.yaml', 'w') as out_file:
            out_file.write(yaml.dump_all(item_dicts))

errors = {
    'noargs': 
    """
    Error: missing arguments. Run this script as
    >>> python rip.py FILEPATH.gb VERSION [DATA_TO_RIP]
    where FILEPATH.gb is a valid path to a ROM file
    & where VERSION is 'r', 'b', 'y', 'Red', 'Blue', or 'Yellow'
    (case-insensitive, leading hyphens allowed, e.g. -r, --red)
    & where [DATA_TO_RIP] is one or more of the following data structures:
        -p, --pkmn, --species             Pokémon species data
        -e, --evo, --evolution,
        -l, --learns, --learnset          Evolutions & Learnsets
        -m, --move, --moves               Move data
        -i, --item, --items               Item data
    (case-insensitive, leading hyphens optional but encouraged for the cool factor)
    """,
    
    'file': 
    """
    Error: invalid filepath. Run this script as
    >>> python rip.py FILEPATH.gb VERSION [DATA_TO_RIP]
    where FILEPATH.gb is a valid path to a ROM file
    """,

    'version': 
    """
    Error: invalid version flag. Run this script as
    >>> python rip.py FILEPATH.gb VERSION [DATA_TO_RIP]
    where VERSION is 'r', 'b', 'y', 'Red', 'Blue', or 'Yellow'
    (case-insensitive, leading hyphens allowed, e.g. -r, --red)
    """,

    'data_flags': 
    """
    Error: invalid data flags. Run this script as
    >>> python rip.py FILEPATH.gb VERSION [DATA_TO_RIP]
    where [DATA_TO_RIP] is one or more of the following data structures:
        -p, --pkmn, --species             Pokémon species data
        -e, --evo, --evolution,
        -l, --learns, --learnset          Evolutions & Learnsets
        -m, --move, --moves               Move data
        -i, --item, --items               Item data
    (case-insensitive, leading hyphens optional but encouraged for the cool factor)
    """
}




if __name__ == '__main__':
    # catch any IndexErrors if 2 command line arguments aren't provided
    try: 
        filepath = sys.argv[1]
        version_flag = sys.argv[2]
        data_to_rip = sys.argv[3:]
    except IndexError:
        print(errors['noargs'])
        sys.exit()

    # interpret & validate version_flag
    version = rby.meta.read_version_flag(version_flag)
    if not version_flag:
        print(errors['version'])
        sys.exit()

    # validate filepath
    if not os.path.exists(filepath):
        print(errors['file'])
        sys.exit()

    # parse other arguments for data structure flags
    data_flags = rby.meta.read_data_flags(data_to_rip)
    if not data_flags:
        print(errors['data_flags'])
        sys.exit()

    main(filepath, version, data_flags)

    
    


