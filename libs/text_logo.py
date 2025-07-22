import json
import pyfiglet

def logo():
    with open("games.json", encoding="utf-8") as f:
        data = json.load(f)

    for game in data:
        title = game.get("name", "Unknown Game")
        try:
            game["description"] = "\n" + pyfiglet.figlet_format(title, width=80)
        except Exception as e:
            game["description"] = f"\n[Figlet error: {e}]\n"

    with open("games.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
