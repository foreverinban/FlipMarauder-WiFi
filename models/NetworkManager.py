from datetime import datetime


class NetworkEntry:
    def __init__(self, wifi_network):
        self.network = wifi_network
        self.first_seen = datetime.now()
        self.last_seen = self.first_seen
        self.hit_count = 1

    def update(self, wifi_network):
        self.network = wifi_network
        self.last_seen = datetime.now()
        self.hit_count += 1


class NetworkManager:
    def __init__(self):
        self.discovered_networks = {}

    def register_network(self, wifinetwork_obj):
        current_bssid = wifinetwork_obj.bssid

        if current_bssid in self.discovered_networks:
            entry = self.discovered_networks[current_bssid]
            entry.update(wifinetwork_obj)
            is_new = False
        else:
            entry = NetworkEntry(wifinetwork_obj)
            self.discovered_networks[current_bssid] = entry
            is_new = True

        return entry.network, is_new

    def get_entries(self) -> list[NetworkEntry]:
        return list(self.discovered_networks.values())

    def get_rows_for_ui(self) -> list[dict]:
        entries = sorted(
            self.discovered_networks.values(),
            key=lambda e: e.hit_count,
            reverse=True,
        )
        return [
            {
                "ssid": e.network.ssid,
                "bssid": e.network.bssid,
                "rssi": e.network.rssi,
                "channel": e.network.channel,
                "encryption": e.network.encryption,
                "hits": e.hit_count,
                "first_seen": e.first_seen,
                "last_seen": e.last_seen,
            }
            for e in entries
        ]
