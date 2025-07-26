import json
import pyfiglet
from lib.paths import *

def logo():
    with open(GAMES_PATH, encoding="utf-8") as f:
        data = json.load(f)

    for game in data:
        title = game.get("name", "Unknown Game")
        try:
            game["description"] = pyfiglet.figlet_format(title, width=80) + "Play "+title+ " on " + game["platform"]
        except Exception as e:
            game["description"] = f"\n[Figlet error: {e}]\n"

    with open(GAMES_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
