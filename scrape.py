## pypkmn/natdex/scrape.py

# script written on 5/17/2022; if script fails, the HTML may have changed

import requests
import bs4
import re

## This script will scrape the pronunciation of Pokémon names from the following webpages:

urls = [
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_I',
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_II',
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_III',
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_IV',
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_V',
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_VI',
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_VII',
    'https://pokemonlp.fandom.com/wiki/Pok%C3%A9mon_Pronunciation_Guide/Generation_VIII',
]

pronunciations = ['']

for url in urls:
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    pronunciation_table_cells = soup.select('.mw-parser-output table ~ table tbody tr ~ tr td:last-child')
    for current_td_cell in pronunciation_table_cells:
        pronunciation = current_td_cell.get_text()
        match = re.match(r'/([\w\W]+)/\n', pronunciation)
        if match:
            pronunciations.append(match.group(1))

with open('out_pronunciations.txt', 'w', encoding='utf8') as file:
    for pronunciation in pronunciations:
        file.write(pronunciation)
        file.write('\n')