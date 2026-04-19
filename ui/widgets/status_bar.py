from datetime import timedelta
from textual.widgets import Static

class ScanStatusBar(Static):
    def __init__(self, port: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self._port = port
        self._count = 0
        self._duration = timedelta(0)
        self._state = "Scanning"
        self._serial_lines = 0
        self._parsed_lines = 0

    def render(self) -> str:
        m, s = divmod(int(self._duration.total_seconds()), 60)
        if self._state in ("Stopped", "Error"):
            hint = "[dim]ESC — back  ↑↓ — scroll[/]"
        else:
            hint = "[dim]Q — stop scan  ESC — back  ↑↓ — scroll[/]"
        return (
            f"[bold cyan]Port:[/] {self._port}  "
            f"[bold cyan]Networks:[/] {self._count}  "
            f"[bold cyan]Lines:[/] {self._serial_lines}/{self._parsed_lines}  "
            f"[bold cyan]Time:[/] {m:02d}:{s:02d}  "
            f"[bold cyan]State:[/] {self._state}  "
            f"{hint}"
        )

    def update_count(self, count: int) -> None:
        self._count = count
        self.refresh()

    def update_duration(self, duration: timedelta) -> None:
        self._duration = duration
        self.refresh()

    def update_state(self, state: str) -> None:
        self._state = state
        self.refresh()

    def update_traffic(self, serial_lines: int, parsed_lines: int) -> None:
        self._serial_lines = serial_lines
        self._parsed_lines = parsed_lines
        self.refresh()
