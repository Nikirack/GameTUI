from textual.command import Hit, Hits, Provider, DiscoveryHit, CommandPalette
import json
from game_launcher import start_game
from lib.paths import *

theme_names = [
    "textual-dark",
    "textual-light",
    "nord",
    "gruvbox",
    "catppuccin-mocha",
    "textual-ansi",
    "dracula",
    "tokyo-night",
    "monokai",
    "flexoki",
    "catppuccin-latte",
    "solarized-light"
]

commands = [
    "launch",
    "Update games",
    "Change theme"
]

class MainCommands(Provider):
    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        for command in commands:
            score = matcher.match(command)
            if score > 0:
                if command == "launch":
                    yield Hit(
                        score,
                        "Launch",
                        command=lambda: self.submenu(Games),
                        help="Launches a game"
                        )
                if command == "Update games":
                    yield Hit(
                        score,
                        "Update games",
                        command=self.app.refresh_games, # type: ignore
                        help="Updates the list of installed games"
                    )
                if command == "Change theme":
                    yield Hit(
                        score,
                        "Change theme",
                        command=lambda: self.submenu(Theme),
                        help="Changes the current theme"
                    )

                    
    async def discover(self) -> Hits:
        for command in commands:
            if command == "launch":
                yield DiscoveryHit(
                    display="Launch",
                    command=lambda: self.submenu(Games),
                    help="Launches a game"
                    )
            if command == "Update games":
                yield DiscoveryHit(
                    display="Update games",
                    command=self.app.refresh_games, # type: ignore
                    help="Updates the list of installed games"
                    )
            if command == "Change theme":
                yield DiscoveryHit(
                    display="Change theme",
                    command=lambda: self.submenu(Theme),
                    help="Changes the current theme"
                )


    def submenu(self,provider):
        palette = CommandPalette(providers=[provider])
        self.app.push_screen(palette)

class Theme(Provider):

    def change_theme(self,name):
        self.app.theme = name

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        for theme in theme_names:
            name = theme.replace("_"," ")
            score = matcher.match(name)
            if score > 0:
                yield Hit(
                    score,
                    name,
                    command=lambda theme=theme: self.change_theme(name=theme),
                    help=f"Changes theme to {theme.replace("_"," ")}"
                )

    async def discover(self) -> Hits:
        for theme in theme_names:
            yield DiscoveryHit(
                display=theme.replace("_"," "),
                command=lambda theme=theme: self.change_theme(name=theme),
                help=f"Changes theme to {theme.replace("_"," ")}"
            )


class Games(Provider):

    def __init__(self, screen, match_style=None):
        super().__init__(screen, match_style)
        self.games = []

    async def startup(self) -> None:
        worker = self.app.run_worker(self.read_files, thread=True)
        self.games = await worker.wait()

    def read_files(self):
        with open(GAMES_PATH, encoding="utf-8") as f:
            return json.load(f)
        
    def returner(self, index):
        success, message = start_game(self.games, index=index)
        self.app.notify(message)

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        for i, game in enumerate(self.games):
            name = game.get("name", "")
            score = matcher.match(name)
            if score > 0:
                yield Hit(
                    score,
                    name,
                    command=lambda i=i: self.returner(index=i),
                    help=f"Launches {name} on {game.get('platform', 'unknown')}"
                )
                
    async def discover(self) -> Hits:
        for i,game in enumerate(self.games):
            name = game.get("name", "Unnamed Game")
            yield DiscoveryHit(
                display=name,
                command=lambda i=i: self.returner(index=i),
                help=f"Launches {name} on {game.get('platform', 'unknown')}"
            )