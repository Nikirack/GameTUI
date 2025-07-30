import json
import lib.game_libraries
import os
import lib.game_libraries.steam
import lib.game_libraries.epic
import lib.description
from lib.paths import *

def merge_data():
    merged_data = {}
    jsons = [STEAM_INFO_PATH, GAMES_INFO_PATH]
    
    for path in jsons:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.update(data)

    with open(MERGED_DATA_PATH, 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=4)

def list_games():
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)

    library = settings["libs"]
    jsons = []
    for lib_name in library:
        if lib_name == "steam":
            lib.game_libraries.steam.get_games()
            jsons.append(STEAM_GAMES_PATH)
        elif lib_name == "epic":
            lib.game_libraries.epic.get_games()
            jsons.append(EPIC_GAMES_PATH)
    merged_data = []
    if os.path.exists(CUSTOM_GAMES_PATH):
        jsons.append(CUSTOM_GAMES_PATH)
    for path in jsons:
        merged_data.extend(json.load(open(path, 'r', encoding='utf-8')))
        if not path == CUSTOM_GAMES_PATH:
            os.remove(path)

    with open(GAMES_PATH, 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=4)
    
    lib.description.logo()