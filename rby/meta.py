## rby/meta.py

import re

def read_version_flag(flag):
    version_regices = {
        'red':    r'^\-*r(ed)?',
        'blue':   r'^\-*b(lue)?',
        'yellow': r'^\-*y(ellow)?'
    }
    
    if flag in version_regices:
        return flag
    for version in version_regices.keys():
        if re.match(version_regices[version], flag, flags=re.IGNORECASE):
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
        'red': 0x038000,
        'blue': 0x038000,
        'yellow': 0x038000
    },

    'items': {
        'red': 0x004608, # source: https://datacrystal.romhacking.net/wiki/Pok%C3%A9mon_Red_and_Blue:ROM_map
        'blue': 0x004608,
        'yellow': 0x004495 # source: http://aurellem.org/vba-clojure/html/rom.html#sec-9-1
    },

    'tm_prices': {
        'red': 0x07BFA7, # source: TechnicalMachinePrices https://web.archive.org/web/20200822125414/https://aww.moe/u408xw.asm
        'blue': 0x07BFA7,
        'yellow': 0xF65F5 # found by searching in Yellow ROM for bytes in Red/Blue - only one matching string
        ## also can compare here, data's the same in all 3 versions: 
        ## https://github.com/pret/pokered/blob/master/data/items/tm_prices.asm
        ## https://github.com/pret/pokeyellow/blob/master/data/items/tm_prices.asm
    }

}


def read_data_flags(flags):
    data_flags = {
        'pkmn': False,
        'basemoves': False,
        'evolutions': False,
        'learnsets': False,
        'moves': False,
        'items': False
    }
    data_structure_regices = {
        'pkmn': r'^\-*p(kmn)?',
        'basemoves': r'^\-*b(ase(moves)?)?',
        'evolutions': r'^\-*e(vo(lutions?)?)?',
        'learnset': r'^\-*l(earns(et)?)?',
        'moves': r'^\-*m(oves?)?',
        'items': r'^\-*i(tems?)?'
    }
    no_match = True

    for current_argument in flags:
        for data_structure in data_structure_regices.keys():
            if re.match(data_structure_regices[data_structure], current_argument, flags=re.IGNORECASE):
                data_flags[data_structure] = True
                no_match = False
        if re.match(r'^\-*species', current_argument, flags=re.IGNORECASE):
            data_flags['pkmn'] = True
            no_match = False
    
    if no_match:
        return False
    else:
        return data_flags