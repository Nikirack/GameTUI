import json
import libs
import os
import libs.steam
import libs.epic
import libs.text_logo

with open("settings.json") as f:
    settings = json.load(f)

library = settings["libs"]

def list_games():
    jsons = []
    for lib in library:
        mod = getattr(libs, lib)
        jsons.append(mod.get_games())

    merged_data = []
    for path in jsons:
        merged_data.extend(json.load(open(path, 'r', encoding='utf-8')))
        os.remove(path)

    with open('games.json', 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=4)
    
    libs.text_logo.logo()