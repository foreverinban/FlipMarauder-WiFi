import re
from models.WiFiNetwork import WiFiNetwork


class MarauderParser:
    # Parses Marauder text output, e.g.:
    # [!] RSSI: -70 Ch: 11 BSSID: AA:BB:CC:DD:EE:FF ESSID: MyWiFi
    # [AP] Ch:6 RSSI:-67 Enc:WPA2 BSSID:AA:BB:CC:DD:EE:FF ESSID:NetworkName

    _BSSID_RE = re.compile(
        r'BSSID:\s*([0-9A-Fa-f]{2}(?:[:\-][0-9A-Fa-f]{2}){5})', re.IGNORECASE
    )
    _RSSI_RE = re.compile(r'RSSI:\s*(-?\d+)', re.IGNORECASE)
    _CH_RE = re.compile(r'Ch(?:annel)?:\s*(\d+)', re.IGNORECASE)
    _ESSID_RE = re.compile(
        r'ESSID:\s*(.+?)(?=\s+(?:BSSID|RSSI|Ch(?:annel)?|Enc(?:ryption)?):|$)',
        re.IGNORECASE,
    )
    _ENC_RE = re.compile(r'Enc(?:ryption)?:\s*(\S+)', re.IGNORECASE)

    def parse_line(self, line: str) -> WiFiNetwork | None:
        bssid_m = self._BSSID_RE.search(line)
        if not bssid_m:
            return None

        rssi_m = self._RSSI_RE.search(line)
        ch_m = self._CH_RE.search(line)
        essid_m = self._ESSID_RE.search(line)

        if not (rssi_m and ch_m and essid_m):
            return None

        enc_m = self._ENC_RE.search(line)

        return WiFiNetwork(
            SSID=essid_m.group(1).strip(),
            BSSID=bssid_m.group(1).upper(),
            RSSI=int(rssi_m.group(1)),
            Channel=int(ch_m.group(1)),
            Encryption=enc_m.group(1) if enc_m else "Unknown",
        )