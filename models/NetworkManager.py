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

    def register_network(self, WiFiNetwork_obj):
        current_BSSID = WiFiNetwork_obj.get_BSSID

        if current_BSSID in self.discovered_networks:
            entry = self.discovered_networks[current_BSSID]
            entry.update(WiFiNetwork_obj)
        else:
            entry = NetworkEntry(WiFiNetwork_obj)
            self.discovered_networks[current_BSSID] = entry
            print(f"New net is detected: {WiFiNetwork_obj.SSID} [{current_BSSID}]")

        return entry.network

    def show_discovered_networks(self):
        print(f"\n{'SSID':<20} | {'BSSID':<18} | {'Hits':<5}")
        print("-" * 50)

        entries = list(self.discovered_networks.values())
        sorted_entries = sorted(entries, key=lambda x: x.hit_count, reverse=True)

        for entry in sorted_entries:
            if entry.hit_count > 1:
                net = entry.network
                print(f"{net.SSID:<20} | {net.get_BSSID:<18} | {entry.hit_count:<5}")
