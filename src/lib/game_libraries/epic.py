import os
import json
from lib.paths import *

MANIFEST_DIR = r"C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests"

def get_epic_games():
    games = []
    if not os.path.exists(MANIFEST_DIR):
        print("Manifest directory not found!")
        return games

    for filename in os.listdir(MANIFEST_DIR):
        if filename.endswith(".item"):
            filepath = os.path.join(MANIFEST_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    game = {
                        "appId": data.get("AppName", ""),
                        "name": data.get("DisplayName", ""),
                        "description": "",
                        "exe": os.path.join(data.get("InstallLocation", ""), data.get("LaunchExecutable", "")) if data.get("InstallLocation") and data.get("LaunchExecutable") else "",
                        "platform": "epic"
                    }
                    games.append(game)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return games

def save_to_json(games, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=4)
    return output_file
    #print(f"Saved {len(games)} games to {output_file}")

def get_games():
    epic_games = get_epic_games()
    games = save_to_json(epic_games, EPIC_GAMES_PATH)
    return games
