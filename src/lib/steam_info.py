import os
import json
import vdf
import datetime

SETTINGS_FILE = "data/settings.json"
OUTPUT_FILE = "data/steam_info.json"

STEAMID64_BASE = 76561197960265728

def find_loginusers_file():
    paths = [
        r"C:\Program Files (x86)\Steam\config\loginusers.vdf",
        os.path.expanduser("~/.steam/steam/config/loginusers.vdf"),
        os.path.expanduser("~/Library/Application Support/Steam/config/loginusers.vdf"),
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("loginusers.vdf not found.")

def find_userdata_folder():
    paths = [
        r"C:\Program Files (x86)\Steam\userdata",
        os.path.expanduser("~/.steam/steam/userdata"),
        os.path.expanduser("~/Library/Application Support/Steam/userdata"),
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Steam userdata folder not found.")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_settings(updated_data):
    settings = load_settings()
    settings.update(updated_data)
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)

def choose_steam_user():
    path = find_loginusers_file()
    with open(path, 'r', encoding='utf-8') as f:
        data = vdf.load(f)

    users = data.get('users', {})
    choices = []
    for steamid, info in users.items():
        choices.append((steamid, info.get("PersonaName", "Unknown User")))

    for i, (_, name) in enumerate(choices):
        print(f"{i + 1}. {name}")
    index = int(input("Select your Steam user (number): ")) - 1
    return choices[index][0]


def convert_timestamp(ts):
    try:
        return datetime.datetime.fromtimestamp(int(ts),tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    except (ValueError, TypeError):
        return None

def parse_playtime(localconfig_path):
    with open(localconfig_path, 'r', encoding='utf-8') as f:
        data = vdf.load(f)

    apps = (
        data.get('Software', {}).get('Valve', {}).get('Steam', {}).get('apps') or
        data.get('UserLocalConfigStore', {}).get('Software', {}).get('Valve', {}).get('Steam', {}).get('apps')
    )

    if not apps:
        return {}

    summary = {}
    for appid, appdata in apps.items():
        if 'Playtime' in appdata:
            summary[appid] = {
                'PlaytimeMinutes': int(appdata['Playtime']),
                'PlaytimeHours': round(int(appdata['Playtime']) / 60, 2),
                'LastPlayed': appdata.get('LastPlayed'),
                'LastPlayedDate': convert_timestamp(appdata.get('LastPlayed')),
            }
    return summary

def main():
    settings = load_settings()
    steamid64 = settings.get("steam_userid")

    if not steamid64:
        steamid64 = choose_steam_user()
        save_settings({"steam_userid": steamid64})

    steamid32 = str(int(steamid64) - STEAMID64_BASE)
    userdata_path = find_userdata_folder()
    localconfig_path = os.path.join(userdata_path, steamid32, 'config', 'localconfig.vdf')

    if not os.path.isfile(localconfig_path):
        raise FileNotFoundError(f"localconfig.vdf not found for SteamID {steamid32}")

    playtime_data = parse_playtime(localconfig_path)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(playtime_data, f, indent=2)