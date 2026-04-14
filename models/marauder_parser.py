import re
from models.WiFiNetwork import WiFiNetwork

# ESP-IDF wifi_auth_mode_t (lower nibble of the trailing auth byte)
auth_map = {
    0: "OPEN",
    1: "WEP",
    2: "WPA",
    3: "WPA2",
    4: "WPA/WPA2",
    5: "Enterprise",
    6: "WPA3",
    7: "WPA2/WPA3",
}

# Actual Marauder scanap output format:
# -62 Ch: 6 44:48:c1:7b:f2:c0 ESSID: ABC 21 04
line_re = re.compile(
    r'^(-?\d+)\s+'                                        # RSSI
    r'Ch:\s*(\d+)\s+'                                     # Channel
    r'([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})\s+'         # BSSID
    r'ESSID:\s*(.*?)\s+(\d+)\s+(\d+)\s*$'                # ESSID + two trailing ints
)

def parse_line(line: str) -> WiFiNetwork | None:
    m = line_re.match(line)
    if not m:
        return None

    rssi, channel, bssid, essid, _, auth_raw = m.groups()

    ssid = essid.strip()
    # Hidden networks: Marauder prints BSSID as ESSID
    if ssid.lower() == bssid.lower():
        ssid = "Hidden Network"

    auth_mode = int(auth_raw) & 0x0F
    encryption = auth_map.get(auth_mode, f"Unknown({auth_raw})")

    return WiFiNetwork(
        ssid=ssid,
        bssid=bssid.upper(),
        rssi=int(rssi),
        channel=int(channel),
        encryption=encryption,
    )
