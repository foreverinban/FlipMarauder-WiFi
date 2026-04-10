import re

class MarauderParser:
    BSSID_PATTERN = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

    def parse_line(self, line : str):
        parts = line.split(',')

        if len(parts) < 6: 
            return None
        SSID = parts[1].strip()
        BSSID = parts[2].strip()

        if not self.BSSID_PATTERN.match(BSSID):
            return None

        try:
            RSSI = int(parts[3].strip())
            Channel = int(parts[4].strip())
        except ValueError:
            print(f"Error: invalid numeric data: RSSI: {parts[3]}, Channel: {parts[4]} in line: {line.strip()}")
            return None
        
        Encryption = parts[5].strip()
        
        current_line = WiFiNetwork(SSID, BSSID, RSSI, Channel, Encryption)
        return DiscoveryEvent(current_line)