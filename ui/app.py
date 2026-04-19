from textual.app import App
from ui.screens.main_menu import MainMenuScreen

class FlipMarauderApp(App):
    CSS_PATH = "app.tcss"

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())