from datetime import datetime


class NetworkEntry:
    def __init__(self, WiFiNetwork):
        self.network = WiFiNetwork
        self.first_seen = datetime.now()
        self.last_seen = self.first_seen
        self.hit_count = 1

    def update(self, WiFiNetwork):
        self.network = WiFiNetwork
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

    def show_discovered_networks(self):
        print(f"\n{'SSID':<25} | {'bssid':<18} | {'Hits':<5} | {'Signal'}")
        print("-" * 75)

        entries = list(self.discovered_networks.values())
        sorted_entries = sorted(entries, key=lambda x: x.hit_count, reverse=True)

        for entry in sorted_entries:
            net = entry.network
            signal = f"{net.rssi} dBm"
            print(f"{net.ssid:<25} | {net.bssid:<18} | {entry.hit_count:<5} | {signal}")
