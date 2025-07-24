import os
import json
from typing import List, Dict, Optional, Any
from lib.vdfparser import parse_vdf 

def normalize_path(p: str) -> str:
    return p.replace('\\\\', '\\')

def parse_steam_library_folders(vdf_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(vdf_path):
        return []

    with open(vdf_path, 'r', encoding='utf-8') as f:
        content = f.read()

    vdf = parse_vdf(content)
    library_data = next(iter(vdf.values())) 

    libraries = []

    for key, entry in library_data.items():
        if not key.isdigit() or not isinstance(entry, dict):
            continue
        path = normalize_path(entry.get("path", ""))
        app_ids = list(entry.get("apps", {}).keys()) if "apps" in entry else []
        libraries.append({
            "path": path,
            "appIds": app_ids
        })

    return libraries

def get_game_name_from_acf(acf_path: str) -> Optional[str]:
    if not os.path.exists(acf_path):
        return None
    with open(acf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        vdf = parse_vdf(content)
        return vdf["AppState"]["name"]
    except Exception:
        return None

BLOCKED_APPIDS = {"228980", "480"}

def get_installed_steam_games(vdf_path: str) -> List[Dict[str, str]]:
    libraries = parse_steam_library_folders(vdf_path)
    games = []

    for library in libraries:
        steamapps_path = os.path.join(str(library['path']), 'steamapps')
        for app_id in library['appIds']:
            if app_id in BLOCKED_APPIDS:
                continue
            acf_path = os.path.join(steamapps_path, f'appmanifest_{app_id}.acf')
            name = get_game_name_from_acf(acf_path)
            if name:
                games.append({
                    'appId': app_id,
                    'name': name,
                    'description': "",
                    'exe': "",
                    'platform': "steam"
                })

    return games

def get_games():
    vdf_path = r'C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf'
    output_path = os.path.join(os.getcwd(), 'steam_games.json')
    games = get_installed_steam_games(vdf_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=4)

    return output_path