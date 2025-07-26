import json
import os
import datetime
from lib.paths import *

def innit():
    if not os.path.exists(GAMES_INFO_PATH):
        with open(GAMES_INFO_PATH, 'w') as f:
            json.dump({}, f)

def create_game_entry(app_id, playtime_minutes, last_played_unix):
    with open(GAMES_INFO_PATH, 'r') as f:
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

    with open(GAMES_INFO_PATH, 'w') as f:
        json.dump(games_data, f, indent=2)