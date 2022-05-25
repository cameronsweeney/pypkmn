import rby.text_encoding, rby.pkmn, rby.moves, rby.items, rby.maps
import rby.tools

import re

data_structures = {
            'pkmn_headers': {
                'order': 'natdex',
                'offset': rby.pkmn.pkmn_header_offset,
                'rip': rby.tools.read_const_length(28),
                'parse': rby.pkmn.parse_pkmn_header
            },
            'evolutions_levelups': {
                'order': 'pkmn',
                'offset': rby.pkmn.evolutions_levelups_offset,
                'rip': rby.tools.read_until(bytearray([0x00, 0x00])),
                'parse': rby.pkmn.parse_evolution_levelup
            },
            'pokedex_info': {
                'order': 'pkmn',
                'offset': rby.pkmn.pokedex_offset,
                'rip': rby.tools.rip_sequence(
                    rby.tools.read_until(bytearray([0x50])),
                    rby.tools.read_const_length(8)
                    ),
                'parse': rby.pkmn.parse_pokedex
            },
            'pokedex_text': {
                'order': 'pkmn',
                'offset': rby.tools.follow_pointer('pokedex_info', 'pokedex_text'),
                'rip': rby.tools.read_until([0x50]),
                'parse': (lambda bytes: {'dex_entry': rby.tools.decode_rby_text(bytes)})
            },
            'move_headers': {
                'order': 'moves',
                'offset': rby.moves.move_header_offset,
                'rip': rby.tools.read_const_length(6),
                'parse': rby.moves.parse_move_bytes
            },
            'item_prices': {
                'order': 'items',
                'offset': rby.items.item_price_offset,
                'rip': rby.tools.read_const_length(3),
                'parse': (lambda bytes: {'price': rby.tools.bcd_decode(bytes)})
            },
            'tm_prices': {
                'order': 'TM',
                'offset': rby.items.tm_price_offset,
                'rip': rby.tools.read_nybble,
                'parse': (lambda byte: {'price': byte*1000})
            },
            'map_headers': {
                'order': 'maps',
                'offset': rby.maps.map_header_offset,
                'rip': rby.tools.rip_sequence(
                    rby.tools.read_const_length(9),
                    rby.maps.read_map_connection_bytes,
                    rby.tools.read_const_length(2)
                    ),
                'parse': rby.maps.parse_map_header
            },
            'map_objects': {
                'order': 'maps',
                'offset': rby.tools.follow_pointer('map_headers', 'map_objects'),
                'rip': rby.tools.pass_offset_to_parser,
                'parse': rby.maps.parse_map_object
            },
            'trainer_teams': {
                'order': 'trainer_classes',
                'offset': rby.maps.trainer_teams_offset,
                'rip': rby.tools.read_until_next_offset,
                'parse': rby.maps.parse_trainer_teams
            },
            'wild_encounters': {
                'order': 'maps',
                'offset': rby.maps.wild_encounters_offset,
                'rip': rby.tools.read_until([0x00, 0x00]),
                'parse': rby.maps.parse_wild_encounters
            }
}

data = {
    'pkmn': {
        'name': 'Pokémon species',
        'regex': r'^\-*p(kmn)?',
        'data_structures': ['pkmn_headers', 'evolutions_learnsets', 'pokedex_info', 'pokedex_entries']
    },
    'moves': {
        'name': 'Pokémon moves',
        'regex': r'^\-*mo(ves?)?',
        'data_structures': ['move_headers']
    },
    'items': {
        'name': 'Items',
        'regex': r'^\-*i(tems?)?',
        'data_structures': ['item_prices', 'tm_prices']
    },
    'maps': {
        'name': 'Maps',
        'regex': r'^\-*maps?',
        'data_structures': ['map_headers', 'map_objects', 'trainer_teams', 'wild_encounters']
    }
}

def read_data_flags(flags):
    data_flags = {
        'pkmn': False,
        'moves': False,
        'items': False,
        'maps': False
    }
    no_match = True

    for current_argument in flags:
        for data_flag in data_flags.keys():
            if re.match(data[data_flag]['regex'], current_argument, flags=re.IGNORECASE):
                data_flags[data_flag] = True
                no_match = False
    
    if no_match:
        return False
    else:
        return data_flags

version_regices = {
    'red':    r'^\-*r(ed)?',
    'blue':   r'^\-*b(lue)?',
    'yellow': r'^\-*y(ellow)?',
    'green': r'^\-*g(reen)?'
}

def read_version_flag(flag):
    if flag in version_regices:
        return flag
    for version in version_regices.keys():
        if re.match(version_regices[version], flag, flags=re.IGNORECASE):
            return version
    return False