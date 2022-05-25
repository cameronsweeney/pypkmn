## Posting Pokémon names & natdex numbers to https://request.cam/pokedex/
## Have to do this before posting RBY data for these Pokémon

import requests
import environs
import yaml

import rby.pokedex

env = environs.Env()
env.read_env()

headers = {
        'content-type': 'application/yaml',
        'authorization': env.str("TOKEN")
    }

error_stack = []

for natdex_number in range(1, 906):
    pkmn = {
        'natdex': natdex_number,
        'name': rby.pokedex.natdex[natdex_number],
        'name_url': rby.pokedex.natdex_url[natdex_number]
    }
    
    pkmn_yaml = yaml.dump(pkmn)

    response = requests.post('https://request.cam/pokedex/', headers=headers, data=pkmn_yaml)
    if response.status_code < 400:
        print(f"Successfully posted YAML for {pkmn['name']} with status code {response.status_code}.")
    else: # add it to the error pile and try again
        print(f"Error when posting YAML for {pkmn['name']}, returned with status code {response.status_code}")
        print(pkmn_yaml)
        error_stack.append(pkmn_yaml)

    if natdex_number in [151, 251, 386, 493, 649, 721, 807]:
        print(f"Just finished posting Pokémon #{natdex_number}. Enter anything to continue.")
        input()

if error_stack:
    print("Printing error_stack to out_errors_pkmn.yaml... Rename this file to try again later.")
    with open('out_errors_pkmn.yaml', 'w') as out_file:
        for error in error_stack:
            out_file.write(error)
            out_file.write('\n---\n')
else:
    print("No requests returned with bad status code. Congrats!")
