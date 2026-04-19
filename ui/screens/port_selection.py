from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Label, ListView, ListItem
from textual.containers import Container
from logic.port_scanner import check_ports
from ui.widgets.logo_widget import LogoWidget
from ui.screens.scan import ScanScreen

class PortSelectionScreen(Screen):
    BINDINGS = [("escape", "go_back", "Back")]

    def __init__(self) -> None:
        super().__init__()
        self._ports: dict[str, str] = {}
        self._back_enabled = False

    def compose(self) -> ComposeResult:
        with Container(id="port-box"):
            yield LogoWidget()
            yield Label("Select Serial Port  (↑↓ + Enter to connect)")
            yield ListView(id="port-list")

    def on_mount(self) -> None:
        # Delay enabling ESC-back to protect against key-repeat cascades
        # when popping from ScanScreen while ESC is held.
        self.set_timer(0.35, self._enable_back)
        self._ports = check_ports()
        lv = self.query_one(ListView)
        if not self._ports:
            lv.append(ListItem(Label("[red]No serial ports found. Connect Flipper and try again.[/red]")))
            return
        for key, device in self._ports.items():
            lv.append(ListItem(Label(f"[cyan][{key}][/cyan]  {device}"), id=f"port-{key}"))

    def _enable_back(self) -> None:
        self._back_enabled = True

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id is None:
            return
        key = event.item.id.removeprefix("port-")
        device = self._ports.get(key)
        if device:
            self.app.push_screen(ScanScreen(port=device))

    def action_go_back(self) -> None:
        if self._back_enabled:
            self.app.pop_screen()
