## rby/rip.py

import yaml
import sys
import os
import functools

import meta
import rby.index

def let_her_rip(rippening, instructions):
    out_filepath = f"rby/{rippening['version']}/{instructions['name']}.yaml"
    ripped_data = {}
    print(f"Ripping data on {instructions['name']} to {out_filepath}...")
    
    for index in rby.index.index[instructions['order']].keys():
        name = rby.index.index[instructions['order']][index]
        #print(name)
        offset = instructions['offset'](rippening, index)
        #print(offset)
        my_bytes = instructions['rip'](rippening, offset)
        #print(my_bytes)
        parsed_data = instructions['parse'](my_bytes, offset)
        #print(parsed_data)
        if isinstance(my_bytes, int):
            hexstr = hex(my_bytes).lstrip('0x').upper().zfill(2)
        elif isinstance(my_bytes, dict):
            # for those cases where data is ripped & parsed together - my_bytes ends up being a dict
            hexstr = parsed_data['binary']
        else:
            hexstr = my_bytes.hex().upper()

        if not isinstance(offset, int):
            # in case offset is an offset_tuple
            offset = offset[0]

        ripped_data[index] = {**parsed_data, 'name': name, 'offset': f'0x{offset:X}', 'binary': hexstr}
        print(f"Ripped #{str(index).zfill(3)}: {name} from 0x{offset:X}\n\n")

    with open(out_filepath, 'w') as out_file:
        out_file.write(yaml.safe_dump(ripped_data))
    print(f"Data written successfully to {out_filepath}.\n\n\n")

    rippening[instructions['name']] = ripped_data
    return rippening

errors = {
    'noargs': 
    """
    Error: missing arguments. Run this script as
    >>> python rip.py FILEPATH.gb VERSION [DATA_TO_RIP]
    """,
    
    'file': 
    """
    where FILEPATH.gb is a valid path to a ROM file
    """,

    'version': 
    """
    where VERSION is 'r', 'b', 'y', 'Red', 'Blue', or 'Yellow'
    (case-insensitive, leading hyphens allowed, e.g. -r, --red)
    """,

    'data_flags': 
    """
    where [DATA_TO_RIP] is one or more of the following data structures:
        -p, --pkmn                      Pokémon species data
        -m, --move, --moves             Move data
        -i, --item, --items             Item data
        -map, --map, --maps             Maps data
    (case-insensitive, leading hyphens optional but encouraged for the cool factor)
    """
}

def write_error_message(error_type):
    print(f"Error: {error_type}. Run this script as\n")
    print(f">>> python {sys.argv[0]}{' FILEPATH.gb' if sys.argv[0]=='rip.py' else ''} VERSION [DATA_TO_RIP]")
    print(errors[error_type])
    sys.exit()

if __name__ == '__main__':
    # first up, validate command line input

    # catch any IndexErrors if 3 command line arguments aren't provided
    try: 
        rom_filepath = sys.argv[1]
        version_flag = sys.argv[2]
        data_to_rip = sys.argv[3:]
    except IndexError:
        write_error_message('noargs')

    # validate filepath
    if not os.path.exists(rom_filepath):
        write_error_message('file')

    # interpret & validate version_flag
    version = meta.read_version_flag(version_flag)
    if not version:
        write_error_message('version')

    # parse other arguments for data structure flags
    data_flags = meta.read_data_flags(data_to_rip)
    if not data_flags:
        write_error_message('data_flags')

    # validation successful, now to start ripping    
    print(f"Running pypkmn/rip.py on {rom_filepath}, which points to a Pokémon {version.title()} ROM...")

    data_structures = []
    for flag in data_flags:
        if data_flags[flag]:
            data_structures += meta.data[flag]['data_structures']
    print(f"Planning to rip the following data structures:\n{data_structures}\n")
    
    print("Reading ROM contents...")
    romdump = []
    with open(rom_filepath, 'rb') as rom:
        romdump = rom.read()

    # fetch functions to calculate offsets, read data, and parse it    
    instructions = map(
        (lambda data_structure: {'name': data_structure, **meta.data_structures[data_structure]}),
        data_structures
        )

    final_rippening = functools.reduce(let_her_rip, instructions, {'romdump': romdump, 'version': version})

    del final_rippening['romdump']
    with open(f'rby/{version}/final.yaml', 'w') as out_file:
        out_file.write(yaml.safe_dump(final_rippening))