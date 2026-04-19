from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button
from textual.containers import Container
from ui.widgets.logo_widget import LogoWidget
from ui.screens.port_selection import PortSelectionScreen

class MainMenuScreen(Screen):
    BINDINGS = [("q", "quit_app", "Quit")]

    def compose(self) -> ComposeResult:
        with Container(id="menu-box"):
            yield LogoWidget()
            yield Button("▶  Start Scan", id="btn-scan", variant="primary")
            yield Button("✕  Exit",       id="btn-exit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-scan":
            self.app.push_screen(PortSelectionScreen())
        elif event.button.id == "btn-exit":
            self.app.exit()

    def action_quit_app(self) -> None:
        self.app.exit()