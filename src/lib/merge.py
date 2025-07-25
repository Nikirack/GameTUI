import json
import lib.game_libraries
import os
import lib.game_libraries.steam
import lib.game_libraries.epic
import lib.description

def merge_data():
    merged_data = {}
    jsons = ["data/steam_info.json", "data/games_info.json"]
    
    for path in jsons:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.update(data)

    with open('data/merged_data.json', 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=4)

def list_games():
    with open("data/settings.json") as f:
        settings = json.load(f)

    library = settings["libs"]
    jsons = []
    for lib_name in library:
        mod = getattr(lib.game_libraries, lib_name)
        jsons.append(mod.get_games())

    merged_data = []
    for path in jsons:
        merged_data.extend(json.load(open(path, 'r', encoding='utf-8')))
        os.remove(path)

    with open('data/games.json', 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=4)
    
    lib.description.logo()