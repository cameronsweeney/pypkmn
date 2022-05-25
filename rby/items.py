def item_price_offset(rippening, index):
    if rippening['version'] == 'yellow':
        return 0x4495 + 3*(index-1) # source: http://aurellem.org/vba-clojure/html/rom.html#sec-9-1
    else: # red or blue
        return 0x4608 + 3*(index-1) # source: https://datacrystal.romhacking.net/wiki/Pok%C3%A9mon_Red_and_Blue:ROM_map

def tm_price_offset(rippening, index):
    nybble = (-1)*((index)%2) # nybble==1 for odd TMs (need high nybble); nybble==-1 for even TMs (need low nybble)
    if rippening['version'] == 'yellow':
        return nybble * (0x0F65F5 + ((index+1) // 2)) # tm_number+1, so that (TM02-1)//2 = 0
        # found by searching in Yellow ROM for the same string of bytes in Red/Blue - only one matching string
    else: # is an HM
        return nybble * (0x07BFA7 + ((index+1) // 2)) # source: TechnicalMachinePrices https://web.archive.org/web/20200822125414/https://aww.moe/u408xw.asm

def read_item_bytes():
    return (lambda rippening, offset: 0 if not offset
            else (rippening['romdump'][offset:offset+3] if offset > 0x6000
                  else (rippening['romdump'][offset])
                )
    )

mart_inventories = {
    # sources: https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9_Mart_data_structure_(Generation_I)#All_Pok.C3.A9_Marts
    # https://github.com/pret/pokered/blob/master/data/items/marts.asm
    # https://web.archive.org/web/20200822125414/https://aww.moe/u408xw.asm -> search "ViridianMartText6:: ; 2442 (0:2442)"
    0x2A: ['Poké Ball', 'Antidote', 'Parlyz Heal', 'Burn Heal'], # Viridian Poké Mart
    0x38: ['Poké Ball', 'Potion', 'Escape Rope', 'Antidote', 'Burn Heal', 'Awakening', 'Parlyz Heal'], # Pewter Poké Mart
    0x43: ['Poké Ball', 'Potion', 'Repel', 'Antidote', 'Burn Heal', 'Awakening', 'Parlyz Heal'], # Cerulean Poké Mart
    0x42: ['Bicycle'], # Cerulean Bike Shop (data unused)
    0x5B: ['Poké Ball', 'Super Potion', 'Ice Heal', 'Awakening', 'Parlyz Heal', 'Repel'], # Vermilion Poké Mart
    0x96: ['Great Ball', 'Super Potion', 'Revive', 'Escape Rope', 'Super Repel', 'Antidote', 'Burn Heal', 'Ice Heal', 'Parlyz Heal'], # Lavender Poké Mart
    0x7B: { # Celadon Department Store 2F - has 2 cashiers
        1: ['Great Ball', 'Super Potion', 'Revive', 'Super Repel', 'Antidote', 'Burn Heal', 'Ice Heal', 'Awakening', 'Parlyz Heal'],
        2: ['TM32', 'TM33', 'TM02', 'TM07', 'TM37', 'TM01', 'TM05', 'TM09', 'TM17'] 
    },
    0x7D: ['Poké Doll', 'Fire Stone', 'Thunder Stone', 'Water Stone', 'Leaf Stone'], # Celadon Department Store 4F
    0x88: { # Celadon Department Store 5F - has 2 cashiers
        1: ['X Accuracy', 'Guard Spec', 'Dire Hit', 'X Attack', 'X Defend', 'X Speed', 'X Special'],
        2: ['HP Up', 'Protein', 'Iron', 'Carbos', 'Calcium']
    },
    0x98: ['Ultra Ball', 'Great Ball', 'Super Potion', 'Revive', 'Full Heal', 'Super Repel'], # Fuchsia Poké Mart
    0xAC: ['Ultra Ball', 'Great Ball', 'Hyper Potion', 'Max Repel', 'Escape Rope', 'Full Heal', 'Revive'], # Cinnabar Poké Mart
    0xB4: ['Great Ball', 'Hyper Potion', 'Max Repel', 'Escape Rope', 'Full Heal', 'Revive'], # Saffron Poké Mart
    0xAE: ['Ultra Ball', 'Great Ball', 'Full Restore', 'Max Potion', 'Full Heal', 'Revive', 'Max Repel'], # Indigo Poké Mart
}
