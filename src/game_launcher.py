import os
import sys
import subprocess
import lib.last_played_other
import lib.steam_info
import time

def start(uri):
    if sys.platform == "win32":
        os.startfile(uri)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", uri])
    else:
        subprocess.Popen(["xdg-open", uri])

def start_game(data, index=None):

    if index is None or not (0 <= index < len(data)):
        return False, "No game selected"

    item = data[index]
    platform = item.get("platform", "").lower()
    app_id = item.get("appId")
    current_timestamp = int(time.time())
    if not platform == "steam":
        lib.last_played_other.create_game_entry(app_id=app_id,playtime_minutes=None,last_played_unix=current_timestamp)
    


    if platform == "steam":
        
        if not app_id:
            return False, f"No Steam app_id for {item['name']}"

        steam_uri = f"steam://run/{app_id}"

        try:
            start(steam_uri)
            lib.steam_info.main()
            return True, f"Launching {item['name']} on Steam"
        except Exception as e:
            return False, f"Failed to launch Steam game: {e}"
    
    elif platform == "epic":
        if not app_id:
            return False, f"No epic app_id for {item['name']}"

        epic_uri = f"com.epicgames.launcher://apps/{app_id}?action=launch&silent=true"

        try:
            start(epic_uri)
            return True, f"Launching {item['name']} on Epic"
        except Exception as e:
            return False, f"Failed to launch Epic game: {e}"

    return False, f"Unsupported platform for {item['name']}"