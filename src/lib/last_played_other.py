import json
import os
import datetime

FILE_PATH = 'data/games_info.json'

def innit():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            json.dump({}, f)

def create_game_entry(app_id, playtime_minutes, last_played_unix):
    with open(FILE_PATH, 'r') as f:
        games_data = json.load(f)
    if playtime_minutes == None:
        games_data[app_id] = {
            "PlaytimeMinutes": None,
            "PlaytimeHours": None,
            "LastPlayed": str(last_played_unix),
            "LastPlayedDate": datetime.datetime.fromtimestamp(int(last_played_unix),tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        }
    else:
        games_data[app_id] = {
            "PlaytimeMinutes": playtime_minutes,
            "PlaytimeHours": round(playtime_minutes / 60, 2),
            "LastPlayed": str(last_played_unix),
            "LastPlayedDate": datetime.datetime.fromtimestamp(int(last_played_unix),tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        }

    with open(FILE_PATH, 'w') as f:
        json.dump(games_data, f, indent=2)