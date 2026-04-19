from datetime import datetime
from textual.screen import Screen
from textual.app import ComposeResult
from textual import work
from textual.binding import Binding
from logic.NetScanner import NetScanner
from ui.events import NetworkDiscovered, ScanError, ScanStopped
from ui.widgets.scan_table import ScanTable
from ui.widgets.status_bar import ScanStatusBar

class ScanScreen(Screen):
    BINDINGS = [
        Binding("q",      "stop_scan", "Stop",    priority=True),
        Binding("escape", "go_back",   "Back",    priority=True),
    ]

    def __init__(self, port: str) -> None:
        super().__init__()
        self._port = port
        self._scanner: NetScanner | None = None
        self._start_time: datetime | None = None
        self._scan_stopped = False
        self._had_error = False

    def compose(self) -> ComposeResult:
        yield ScanTable(id="scan-table")
        yield ScanStatusBar(port=self._port, id="status-bar")

    def on_mount(self) -> None:
        self._scanner = NetScanner(self._port)
        self._start_time = datetime.now()
        self.query_one(ScanStatusBar).update_state("Scanning")
        self._scan_worker()
        self._refresh_timer = self.set_interval(2.0, self._refresh_table)
        self._tick_timer = self.set_interval(1.0, self._tick_status)

    @work(thread=True)
    def _scan_worker(self) -> None:
        scanner = self._scanner
        if scanner is None:
            self.post_message(ScanStopped())
            return
        try:
            for network in scanner.start_scan():
                entry = scanner.manager.discovered_networks.get(network.bssid)
                hit_count = entry.hit_count if entry else 1
                self.post_message(NetworkDiscovered(network, hit_count))
        except Exception as exc:
            self.post_message(ScanError(exc))
        finally:
            self.post_message(ScanStopped())

    def on_network_discovered(self, event: NetworkDiscovered) -> None:
        self.query_one(ScanTable).upsert_network(event.network, event.hit_count)
        scanner = self._scanner
        if scanner is None:
            return
        count = len(scanner.manager.discovered_networks)
        self.query_one(ScanStatusBar).update_count(count)

    def on_scan_error(self, event: ScanError) -> None:
        self._had_error = True
        self.query_one(ScanStatusBar).update_state("Error")
        self.notify(str(event.error), severity="error")

    def on_scan_stopped(self, _: ScanStopped) -> None:
        if self._scan_stopped:
            return
        self._scan_stopped = True
        self._refresh_timer.stop()
        self._tick_timer.stop()
        status = self.query_one(ScanStatusBar)
        if not self._had_error:
            status.update_state("Stopped")
        self._refresh_table()

        network_count = (
            len(self._scanner.manager.discovered_networks) if self._scanner else 0
        )
        if network_count == 0 and self._scanner:
            if self._scanner.total_serial_lines == 0:
                self.notify(
                    "No serial data received. Is Flipper connected?",
                    severity="warning",
                )
            elif self._scanner.parsed_network_lines == 0:
                self.notify(
                    "Data received but no AP rows parsed.",
                    severity="warning",
                )
            else:
                self.notify("No access points found.", severity="information")
        else:
            self.notify(
                f"Scan stopped — {network_count} network(s) found. Press ESC to go back.",
                severity="information",
            )

    def action_stop_scan(self) -> None:
        """Q — stop the scan (stays on screen so user can see results)."""
        if self._scan_stopped:
            return
        if self._scanner:
            self.query_one(ScanStatusBar).update_state("Stopping...")
            self._scanner.stop_scan()

    def action_go_back(self) -> None:
        """ESC — stop if running, then go back to port selection."""
        if not self._scan_stopped and self._scanner:
            self._scanner.stop_scan()
        self.app.pop_screen()

    def _refresh_table(self) -> None:
        scanner = self._scanner
        if scanner:
            rows = scanner.manager.get_rows_for_ui()
            self.query_one(ScanTable).refresh_rows(rows)

    def _tick_status(self) -> None:
        scanner = self._scanner
        status = self.query_one(ScanStatusBar)
        if scanner:
            status.update_traffic(scanner.total_serial_lines, scanner.parsed_network_lines)
        if self._start_time:
            status.update_duration(datetime.now() - self._start_time)

    def on_unmount(self) -> None:
        if self._scanner and not self._scan_stopped:
            self._scanner.stop_scan()
