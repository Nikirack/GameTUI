import json
import lib
import os
import lib.game_libraries.steam
import lib.game_libraries.epic
import lib.description

with open("settings.json") as f:
    settings = json.load(f)

library = settings["libs"]

def list_games():
    jsons = []
    for lib_name in library:
        mod = getattr(lib, lib_name)
        jsons.append(mod.get_games())

    merged_data = []
    for path in jsons:
        merged_data.extend(json.load(open(path, 'r', encoding='utf-8')))
        os.remove(path)

    with open('games.json', 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=4)
    
    lib.description.logo()