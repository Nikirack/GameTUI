import json
from lib.paths import *

standard_settings = {
    "theme": "nord",
    "libs": [
        "steam",
        "epic"
    ]
}

def gen_settings():
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as outfile:
        json.dump(standard_settings, outfile, indent=4)