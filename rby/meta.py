## rby/meta.py

import re

regices = {
    'red':    r'^\-*r(ed)?',
    'blue':   r'^\-*b(lue)?',
    'yellow': r'^\-*y(ellow)?'
}

def read_version_flag(flag):
    if flag in regices:
        return flag
    for version in regices.keys():

        if re.match(regices[version], flag, flags=re.IGNORECASE):
            return version
    return False

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
