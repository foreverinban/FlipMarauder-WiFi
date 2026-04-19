from textual.widgets import DataTable
from textual.widgets.data_table import CellDoesNotExist

class ScanTable(DataTable):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self._row_keys: set[str] = set()
        self.add_column("SSID", key="SSID")
        self.add_column("BSSID", key="BSSID")
        self.add_column("RSSI",  key="RSSI")
        self.add_column("CH",    key="CH")
        self.add_column("ENC",   key="ENC")
        self.add_column("Hits",  key="Hits")

    def upsert_network(self, network, hit_count) -> None:
        if network.bssid in self._row_keys:
            self.update_cell(network.bssid, "RSSI", str(network.rssi))
            self.update_cell(network.bssid, "Hits", str(hit_count))
            return

        try:
            self.add_row(
                network.ssid, 
                network.bssid, 
                str(network.rssi),
                str(network.channel),
                network.encryption,
                str(hit_count),
                key=network.bssid,
            )
            self._row_keys.add(network.bssid)
        except CellDoesNotExist:
            # Fallback for racey redraw edge-cases.
            self.update_cell(network.bssid, "RSSI", str(network.rssi))
            self.update_cell(network.bssid, "Hits", str(hit_count))

    def refresh_rows(self, rows: list[dict]) -> None:
        for row in rows:
            bssid = row["bssid"]
            if bssid in self._row_keys:
                self.update_cell(bssid, "RSSI", str(row["rssi"]))
                self.update_cell(bssid, "Hits", str(row["hits"]))
                continue
            try:
                self.add_row(
                    row["ssid"],
                    bssid,
                    str(row["rssi"]),
                    str(row["channel"]),
                    row["encryption"],
                    str(row["hits"]),
                    key=bssid,
                )
                self._row_keys.add(bssid)
            except CellDoesNotExist:
                self.update_cell(row["bssid"], "RSSI", str(row["rssi"]))
                self.update_cell(row["bssid"], "Hits", str(row["hits"]))
