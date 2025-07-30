from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import Input, Button, Label
from textual.screen import ModalScreen
import json, os
from lib.paths import *

class CustomGameScreen(ModalScreen):
    CSS = """
    CustomGameScreen {
        align: center middle;
    }
    #dialog {
        grid-size: 1;
        grid-gutter: 1 2;
        padding: 0 1;
        width: 60;
        height: auto;
        background: $surface;
        border: thick $background;
    }

    #title {
        content-align: center middle;
        height: 1;
    }

    #error_label {
        color: red;
        height: 1;
    content-align: center middle;
    }

    Button {
        width: 100%;
    }

    Input {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Add New Game", id="title"),
            Input(placeholder="Game Name", id="name_input"),
            Input(placeholder="Full Path to Game EXE", id="path_input"),
            Label("", id="error_label"),
            Button("Save", id="save_button"),
            Button("Cancel", id="cancel_button"),
            id="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed):
        name = self.query_one("#name_input", Input).value.strip()
        path = self.query_one("#path_input", Input).value.strip()
        error_label = self.query_one("#error_label", Label)

        if event.button.id == "cancel_button":
            self.dismiss(None)
            return

        if not name or not path:
            error_label.update("Name and path are required.")
            return
        path = path.replace('"','')
        if not os.path.exists(path):
            error_label.update("Path does not exist.")
            return

        if os.path.exists(CUSTOM_GAMES_PATH):
            with open(CUSTOM_GAMES_PATH, "r", encoding="utf-8") as f:
                games = json.load(f)
        else:
            games = []

        games.append({
            "appId":f"Cus{abs(hash(name))}",
            "name": name,
            "description":"",
            "exe": path,
            "platform":"custom"
            })
        
        with open(CUSTOM_GAMES_PATH, "w", encoding="utf-8") as f:
            json.dump(games, f, indent=2)

        self.dismiss({"name": name})