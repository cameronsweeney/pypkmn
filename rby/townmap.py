## rby/townmap.py

## collection of internal RBY indices & data related to maps
## map_index, wild_encounter_percents, wild_encounter_per256
## grass_maps, indoor_maps, cave_maps, land_encounter_type(map_id)
## rb_fish_groups_by_map

map_index = {
    ################################################################################
    ###  source: https://github.com/pret/pokemon-reverse-engineering-tools/blob/ ###
    ###  5e0715f2579adcfeb683448c9a7826cfd3afa57d/redtools/extract_maps.py#L27   ###
    ################################################################################
    0x00: "Pallet Town",
    0x01: "Viridian City",
    0x02: "Pewter City",
    0x03: "Cerulean City",
    0x04: "Lavender Town",
    0x05: "Vermilion City",
    0x06: "Celadon City",
    0x07: "Fuchsia City",
    0x08: "Cinnabar Island",
    0x09: "Indigo Plateau",
    0x0A: "Saffron City",

    0x0C: "Route 1",
    0x0D: "Route 2",
    0x0E: "Route 3",
    0x0F: "Route 4",
    0x10: "Route 5",
    0x11: "Route 6",
    0x12: "Route 7",
    0x13: "Route 8",
    0x14: "Route 9",
    0x15: "Route 10",
    0x16: "Route 11",
    0x17: "Route 12",
    0x18: "Route 13",
    0x19: "Route 14",
    0x1A: "Route 15",
    0x1B: "Route 16",
    0x1C: "Route 17",
    0x1D: "Route 18",
    0x1E: "Route 19",
    0x1F: "Route 20",
    0x20: "Route 21",
    0x21: "Route 22",
    0x22: "Route 23",
    0x23: "Route 24",
    0x24: "Route 25",
    0x25: "Pallet Red's House 1F",
    0x26: "Pallet Red's House 2F",
    0x27: "Pallet Blue's House",
    0x28: "Pallet Professor Oak's Laboratory",
    0x29: "Viridian Pokémon Center",
    0x2A: "Viridian Poké Mart",
    0x2B: "Viridian Trainers' School",
    0x2C: "Viridian House",
    0x2D: "Viridian Gym",
    0x2E: "Route 2 Diglett's Cave Entrance",
    0x2F: "Viridian Forest North Gate",
    0x30: "Route 2 House",
    0x31: "Route 2 Gate",
    0x32: "Viridian Forest South Gate",
    0x33: "Viridian Forest",
    0x34: "Pewter Museum 1F",
    0x35: "Pewter Museum 2F",
    0x36: "Pewter Gym",
    0x37: "Pewter House NE",
    0x38: "Pewter Poké Mart",
    0x39: "Pewter House SW",
    0x3A: "Pewter Pokémon Center",
    0x3B: "Mt. Moon 1F",
    0x3C: "Mt. Moon B1",
    0x3D: "Mt. Moon B2",
    0x3E: "Cerulean House (Trashed)",
    0x3F: "Cerulean House (Trade)",
    0x40: "Cerulean Pokémon Center",
    0x41: "Cerulean Gym",
    0x42: "Cerulean Bike Shop",
    0x43: "Cerulean Poké Mart",
    0x44: "Mt. Moon Pokémon Center",
    0x46: "Route 5 Gate",
    0x47: "Route 5 Underground Path Entrance",
    0x48: "Route 5 Day Care",
    0x49: "Route 6 Gate",
    0x4A: "Route 6 Underground Path Entrance",
    0x4C: "Route 7 Gate",
    0x4D: "Route 7 Underground Path Entrance",
    0x4F: "Route 8 Gate",
    0x50: "Route 8 Underground Path Entrance",
    0x51: "Rock Tunnel Pokémon Center",
    0x52: "Rock Tunnel 1F",
    0x53: "Power Plant",
    0x54: "Route 11 Gate 1F",
    0x55: "Route 11 Diglett's Cave Entrance",
    0x56: "Route 11 Gate 2F",
    0x57: "Route 12 Gate 1F",
    0x58: "Route 25 Bill's House",
    0x59: "Vermilion Pokémon Center",
    0x5A: "Vermilion Pokémon Fan Club",
    0x5B: "Vermilion Poké Mart",
    0x5C: "Vermilion Gym",
    0x5D: "Vermilion House SE",
    0x5E: "Vermilion Dock",
    0x5F: "S.S. Anne 1F Corridor",
    0x60: "S.S. Anne 2F Corridor",
    0x61: "S.S. Anne Corridor to Deck",
    0x62: "S.S. Anne B1 Corridor",
    0x63: "S.S. Anne Deck",
    0x64: "S.S. Anne Kitchen",
    0x65: "S.S. Anne Captain's Room",
    0x66: "S.S. Anne 1F Rooms",
    0x67: "S.S. Anne 2F Rooms",
    0x68: "S.S. Anne B1 Rooms",
    0x6C: "Victory Road 1F",
    0x71: "Indigo Plateau Lance's Room",
    0x76: "Indigo Plateau Hall of Fame Room",
    0x77: "Underground Path (N/S)",
    0x78: "Indigo Plateau Champion's Room",
    0x79: "Underground Path (W/E)",
    0x7A: "Celadon Department Store 1F",
    0x7B: "Celadon Department Store 2F",
    0x7C: "Celadon Department Store 3F",
    0x7D: "Celadon Department Store 4F",
    0x7E: "Celadon Department Store Roof",
    0x7F: "Celadon Department Store Elevator",
    0x80: "Celadon Mansion 1F",
    0x81: "Celadon Mansion 2F",
    0x82: "Celadon Mansion 3F",
    0x83: "Celadon Mansion Rooftop",
    0x84: "Celadon Mansion Rooftop Room",
    0x85: "Celadon Pokémon Center",
    0x86: "Celadon Gym",
    0x87: "Celadon Game Corner",
    0x88: "Celadon Department Store 5F",
    0x89: "Celadon Game Corner Prize Exchange",
    0x8A: "Celadon Diner",
    0x8B: "Celadon House",
    0x8C: "Celadon Hotel",
    0x8D: "Lavender Pokémon Center",
    0x8E: "Pokémon Tower 1F",
    0x8F: "Pokémon Tower 2F",
    0x90: "Pokémon Tower 3F",
    0x91: "Pokémon Tower 4F",
    0x92: "Pokémon Tower 5F",
    0x93: "Pokémon Tower 6F",
    0x94: "Pokémon Tower 7F",
    0x95: "Lavender Mr. Fuji's House",
    0x96: "Lavender Poké Mart",
    0x97: "Lavender House SW",
    0x98: "Fuchsia Poké Mart",
    0x99: "Fuchsia House SW",
    0x9A: "Fuchsia Pokémon Center",
    0x9B: "Fuchsia Warden's House",
    0x9C: "Safari Zone Entrance",
    0x9D: "Fuchsia Gym",
    0x9E: "Safari Zone Meeting Room",
    0x9F: "Seafoam Islands B1",
    0xA0: "Seafoam Islands B2",
    0xA1: "Seafoam Islands B3",
    0xA2: "Seafoam Islands B4",
    0xA3: "Vermilion Fishing Guru's House",
    0xA4: "Fuchsia Fishing Guru's Older Brother's House",
    0xA5: "Pokémon Mansion 1F",
    0xA6: "Cinnabar Gym",
    0xA7: "Cinnabar Pokémon Lab Entrance",
    0xA8: "Cinnabar Pokémon Lab Meeting Room",
    0xA9: "Cinnabar Pokémon Lab R&D Room",
    0xAA: "Cinnabar Pokémon Lab Testing Room",
    0xAB: "Cinnabar Pokémon Center",
    0xAC: "Cinnabar Poké Mart",
    0xAE: "Indigo Plateau Lobby",
    0xAF: "Saffron Copycat's House 1F",
    0xB0: "Saffron Copycat's House 2F",
    0xB1: "Saffron Fighting Dojo",
    0xB2: "Saffron Gym",
    0xB3: "Saffron House NW",
    0xB4: "Saffron Poké Mart",
    0xB5: "Silph Co 1F",
    0xB6: "Saffron Pokémon Center",
    0xB7: "Saffron Mr. Psychic's House",
    0xB8: "Route 15 Gate 1F",
    0xB9: "Route 15 Gate 2F",
    0xBA: "Route 16 Gate 1F",
    0xBB: "Route 16 Gate 2F",
    0xBC: "Route 16 House",
    0xBD: "Route 12 House",
    0xBE: "Route 18 Gate 1F",
    0xBF: "Route 18 Gate 2F",
    0xC0: "Seafoam Islands 1F",
    0xC1: "Route 22 Gate",
    0xC2: "Victory Road 2F",
    0xC3: "Route 12 Gate 2F",
    0xC4: "Vermilion House (Trade)",
    0xC5: "Diglett's Cave",
    0xC6: "Victory Road 3F",
    0xC7: "Rocket Hideout B1",
    0xC8: "Rocket Hideout B2",
    0xC9: "Rocket Hideout B3",
    0xCA: "Rocket Hideout B4",
    0xCB: "Rocket Hideout Elevator",
    0xCF: "Silph Co. 2F",
    0xD0: "Silph Co. 3F",
    0xD1: "Silph Co. 4F",
    0xD2: "Silph Co. 5F",
    0xD3: "Silph Co. 6F",
    0xD4: "Silph Co. 7F",
    0xD5: "Silph Co. 8F",
    0xD6: "Pokémon Mansion 2F",
    0xD7: "Pokémon Mansion 3F",
    0xD8: "Pokémon Mansion 4F",
    0xD9: "Safari Zone East",
    0xDA: "Safari Zone North",
    0xDB: "Safari Zone West",
    0xDC: "Safari Zone Center",
    0xDD: "Safari Zone Center Rest House",
    0xDE: "Safari Zone Secret House",
    0xDF: "Safari Zone West Rest House",
    0xE0: "Safari Zone East Rest House",
    0xE1: "Safari Zone North Rest House",
    0xE2: "Cerulean Cave 2F",
    0xE3: "Cerulean Cave B1",
    0xE4: "Cerulean Cave 1F",
    0xE5: "Lavender Name Rater's House",
    0xE6: "Cerulean House (Badges)",
    0xE8: "Rock Tunnel B1",
    0xE9: "Silph Co. 9F",
    0xEA: "Silph Co. 10F",
    0xEB: "Silph Co. 11F",
    0xEC: "Silph Co. Elevator",
    0xEF: "Battle Center",
    0xF0: "Trade Center",
    0xF5: "Indigo Plateau Lorelei's Room",
    0xF6: "Indigo Plateau Bruno's Room",
    0xF7: "Indigo Plateau Agatha's Room"
}

grass_maps = [
    0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13,
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B,
    0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23,
    0x24, # Routes 1 to 25
    
    0xD9, 0xDA, 0xDB, 0xDC # Safari Zone maps
]

indoor_maps = [
    0x53, # Power Plant
    0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, # Pokémon Tower 1F-7F
    0xA5, 0xD6, 0xD7, 0xD8, # Pokémon Mansion 1F-4F
]

cave_maps = [
    0x3B, 0x3C, 0x3D, # Mt. Moon 1F, B1, B2
    0x52, 0xE8, # Rock Tunnel 1F, B1
    0x6C, 0xC2, 0xC6, # Victory Road 1F-3F
    0x9F, 0xA0, 0xA1, 0xA2, 0xC0, # Seafoam Islands B1-B4, 1F
    0xC5, # Diglett's Cave
    0xE2, 0xE3, 0xE4, # Cerulean Cave 2F, B1, 1F
]

def land_encounter_type(map_id):
    # pass a map id to this function and it will return a string describing the type of land encounter
    # returns False if map has no land encounters
    # In Gen I there's outside grass encounters, caves with wild Pokémon, and a few indoor locations
    if map_id in grass_maps:
        return 'tall grass'
    elif map_id in indoor_maps:
        return 'indoors'
    elif map_id in cave_maps:
        return 'cave'
    else:
        return False

## https://github.com/pret/pokered/blob/master/data/wild/probabilities.asm
land_encounter_percents = [20, 20, 15, 10, 10, 10, 5, 5, 4, 1]
land_encounter_per256   = [51, 51, 39, 25, 25, 25, 13, 13, 11, 3]

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