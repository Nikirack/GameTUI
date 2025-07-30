from textual.app import App, ComposeResult
from textual.command import CommandPalette
from textual.widgets import Static, Footer, Header
from textual.widgets import ListView, ListItem, Label
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.binding import Binding
from textual.events import Key
import json
import os
from commands import MainCommands, Games
from game_launcher import start_game
import lib.merge
import lib.settings
import lib.steam_info
import lib.last_played_other
from lib.paths import *

class DescriptionPanel(Static):
    text: reactive[str] = reactive("")

    def watch_text(self, new_text: str) -> None:
        self.update(new_text)


class GameLauncher(App):
    COMMAND_PALETTE_BINDING = "colon"
    COMMANDS = {MainCommands}
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="j", action="", description="Move the cursor down",show=False),
        Binding(key="k", action="", description="Move the cursor up",show=False)
    ]
    CSS_PATH = "css.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        self.list_view = ListView()
        self.description_panel = DescriptionPanel()
        yield Horizontal(
            self.list_view,
            self.description_panel,
        )
        yield Footer()
        
    def on_mount(self):
        self.title = "TUI Game Launcher"
        with open(GAMES_PATH, encoding="utf-8") as f:
            self.data = json.load(f)
        with open(SETTINGS_PATH) as f:
            self.settings = json.load(f)

        self.sort_games_by_last_played()

        for item in self.data:
            self.list_view.append(ListItem(Label(item["name"])))

        if self.data:
            self.update_description(0)
        
        self.theme = self.settings["theme"]
        self.palette_open = False

    def on_key(self, event: Key) -> None:
        if event.key == "j":
            self.list_view.action_cursor_down()
        elif event.key == "k":
            self.list_view.action_cursor_up()
        elif event.key == "enter":
            if self.palette_open == False:
                self.launch_game()


    def on_command_palette_opened(self, event: CommandPalette.Opened) -> None:
        self.palette_open = True

    def on_command_palette_closed(self, event: CommandPalette.Closed) -> None:
        self.palette_open = False

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if self.list_view.index is not None:
            self.update_description(self.list_view.index)

    def watch_theme(self, old_value: str, new_value: str):
        if self.settings["theme"] != new_value:
            self.notify(f"Theme changed from {old_value} to {new_value}")
            self.settings["theme"] = new_value
            with open(SETTINGS_PATH, "w") as file:
                json.dump(self.settings, file, indent=4)

    def launch_game(self):
        index = self.list_view.index
        success, message = start_game(self.data, index=index)
        self.notify(message)
        lib.merge.merge_data()
        self.refresh_games()

    def update_description(self, index: int):
        if 0 <= index < len(self.data):
            self.description_panel.text = self.data[index]["description"]

    def refresh_games(self):
        lib.merge.list_games()
        self.list_view.clear()
        with open(GAMES_PATH, encoding="utf-8") as f:
            self.data = json.load(f)
        self.sort_games_by_last_played()
        for item in self.data:
            self.list_view.append(ListItem(Label(item["name"])))
        if self.data:
            self.update_description(0)

    def sort_games_by_last_played(self):
        with open(MERGED_DATA_PATH, encoding="utf-8") as f:
            game_info = json.load(f)

        def get_last_played(game):
            app_id = game.get("appId")
            if app_id and app_id in game_info:
                return int(game_info[app_id].get("LastPlayed", 0))
            return 0

        self.data.sort(key=get_last_played, reverse=True)

app = GameLauncher()
if __name__ == "__main__":
    if not os.path.exists(GAMES_INFO_PATH):
        with open(GAMES_INFO_PATH, 'w') as f:
            json.dump({}, f)
    if os.path.exists(SETTINGS_PATH):
        if not os.path.exists(GAMES_PATH):
            lib.merge.list_games()
    else:
        lib.settings.gen_settings()
        if not os.path.exists(GAMES_PATH):
            lib.merge.list_games()
    lib.steam_info.main()
    lib.merge.merge_data()
    app.run()
