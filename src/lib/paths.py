import os
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

GAMES_INFO_PATH = os.path.join(DATA_DIR, "games_info.json")
GAMES_PATH = os.path.join(DATA_DIR, "games.json")
MERGED_DATA_PATH = os.path.join(DATA_DIR, "merged_data.json")
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.json")
STEAM_INFO_PATH = os.path.join(DATA_DIR, "steam_info.json")
STEAM_GAMES_PATH = os.path.join(DATA_DIR, "steam_games.json")
EPIC_GAMES_PATH = os.path.join(DATA_DIR, "epic_games.json")
CUSTOM_GAMES_PATH = os.path.join(DATA_DIR, "custom_games.json")