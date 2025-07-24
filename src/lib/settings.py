import json

standard_settings = {
    "theme": "nord",
    "libs": [
        "steam",
        "epic"
    ]
}

def gen_settings():
    with open('settings.json', 'w', encoding='utf-8') as outfile:
        json.dump(standard_settings, outfile, indent=4)