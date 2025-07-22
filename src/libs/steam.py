import os
import json
import re

from typing import List, Dict, Optional, Any

def normalize_path(p: str) -> str:
    return p.replace('\\\\', '\\')

def parse_steam_library_folders(vdf_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(vdf_path):
        return []
    with open(vdf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    libraries = []
    current_path = None
    in_apps = False
    app_ids = []

    for line in lines:
        line = line.strip()
        if line.startswith('"path"'):
            match = re.search(r'"path"\s+"(.+?)"', line)
            if match:
                current_path = normalize_path(match.group(1))
                app_ids = []
        if line.startswith('"apps"'):
            in_apps = True
            continue
        if in_apps and line.startswith('}'):
            if current_path:
                libraries.append({'path': current_path, 'appIds': list(app_ids)})
                current_path = None
                app_ids = []
            in_apps = False
            continue
        if in_apps:
            app_match = re.match(r'"(\d+)"\s+"', line)
            if app_match:
                app_ids.append(app_match.group(1))
    return libraries

def get_game_name_from_acf(acf_path: str) -> Optional[str]:
    if not os.path.exists(acf_path):
        return None
    with open(acf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    name_match = re.search(r'"name"\s+"(.+?)"', content)
    return name_match.group(1) if name_match else None

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
                    'exe':"",
                    'platform':"steam"
                })
    return games

def get_games():
    vdf_path = r'C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf'
    output_path = os.path.join(os.getcwd(), 'steam_games.json')
    games = get_installed_steam_games(vdf_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=4)

    return output_path


