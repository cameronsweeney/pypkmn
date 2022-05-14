import requests
import environs
import sys
import os
import yaml

import rby.tools, rby.meta

url_endpoints = {
    'pkmn': 'pkmn/rby/',
    'basemoves': 'moves/levelup/',
    'evolutions': 'pkmn/evolutions/',
    'learnsets': 'moves/levelup/',
    'moves': 'moves/',
    'items': 'items/'
}

def post_data(data_structure, yaml_list):
    env = environs.Env()
    env.read_env()
    token = env.str("TOKEN")

    headers = {
        'content-type': 'application/yaml',
        'authorization': token
    }
    error_stack = []

    url = 'https://request.cam/pokedex/' + url_endpoints[data_structure]

    if data_structure == 'basemoves':
        # this means we're just posting the learnbase from each Pokémon, not the whole species data header
        # all other data structures get ripped in a format that can be posted directly to request.cam
        yaml_list = rby.tools.get_learnbases_only(yaml_list)

    for current_obj in yaml_list:
        response = requests.post(url, headers=headers, data=current_obj)
        if response.status_code == 201: # add it to the error pile and try again
            print(f"Success: {response.status_code} when posting YAML.")
        else:
            print(f"Error: {response.status_code} when posting the following YAML to {url}:")
            print(current_obj)
            error_stack.append(current_obj)

    if error_stack:
        print(f"Total of {len(error_stack)} YAML objects failed to post. Try again? [y/n]")
        answer = input()
        if answer == 'y':
            post_data(data_structure, error_stack)
        else:
            out_filepath = f"out_errors_{data_structure}.yaml"
            print(f"Printing error_stack to {out_filepath}... Rename this file to try again later.")
            with open(out_filepath, 'w') as out_file:
                out_file.write('\n---\n'.join(error_stack))


errors = {
    'noargs':
    """
    Error: missing arguments. Run this script as
    >>> python post.py VERSION [DATA_TO_POST]
    where VERSION is 'r', 'b', 'y', 'Red', 'Blue', or 'Yellow'
    (case-insensitive, leading hyphens allowed, e.g. -r, --red)
    & where [DATA_TO_POST] is one or more of the following data structures:
        -p, --pkmn, --species             Pokémon species data
        -b, --base, --basemoves           Pokémon base moves (known at Lv.1)
        -e, --evo, --evolution            Evolutions
        -l, --learns, --learnset          Learnsets
        -m, --move, --moves               Move data
        -i, --item, --items               Item data
    (case-insensitive, leading hyphens optional but encouraged for the cool factor)
    """,

    'version': 
    """
    Error: invalid version flag. Run this script as
    >>> python post.py VERSION [DATA_TO_POST]
    where VERSION is 'r', 'b', 'y', 'Red', 'Blue', or 'Yellow'
    (case-insensitive, leading hyphens allowed, e.g. -r, --red)
    """,

    'data_flags': """
    Error: missing arguments. Run this script as
    >>> python post.py VERSION [DATA_TO_POST]
    where [DATA_TO_POST] is one or more of the following data structures:
        -p, --pkmn, --species             Pokémon species data
        -b, --base, --basemoves           Pokémon base moves (known at Lv.1)
        -e, --evo, --evolution            Evolutions
        -l, --learns, --learnset          Learnsets
        -m, --move, --moves               Move data
        -i, --item, --items               Item data
    (case-insensitive, leading hyphens optional but encouraged for the cool factor)
    """,
}

if __name__ == '__main__':
    # catch any IndexErrors if 2 command line arguments aren't provided
    try: 
        version_flag = sys.argv[1]
        data_to_rip = sys.argv[2:]
    except IndexError:
        print(errors['noargs'])
        sys.exit()

    # interpret & validate version_flag
    version = rby.meta.read_version_flag(version_flag)
    if not version_flag:
        print(errors['version'])
        sys.exit()

    data_flags = rby.meta.read_data_flags(data_to_rip)
    if not data_flags:
        print(errors['data_flags'])
        sys.exit()

    print(f"Running pypkmn/post.py for data ripped from Pokémon {version.title()}...")

    for data_structure in data_flags:
        filename = data_structure
        if data_structure == 'basemoves':
            filename = 'pkmn'
        if data_flags[data_structure]:
            filepath = f'rby/{version}/{filename}.yaml'
            if not os.path.exists(filepath):
                print(f"Error: required file missing at {filepath}. Make sure to rip the data before trying to post it.")
                sys.exit()
            print(f"Reading in data for {data_structure} from {filepath}...")
            with open(filepath, 'r') as in_file:
                in_yaml = in_file.read()
            list_of_yaml = in_yaml.split('---')
            post_data(data_structure, list_of_yaml)