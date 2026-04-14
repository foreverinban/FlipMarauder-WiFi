import math
from dataclasses import dataclass

@dataclass(slots=True)
class WiFiNetwork:
    ssid : str
    bssid : str
    rssi : float
    channel : int
    encryption : str

    @property
    def rssi_rate(rssi) -> str:

        val = math.ceil(rssi)

        if rssi >= -50:
            return f"Very Good Signal Strenght - {val} dbm"
        if -60 <= val <= -51:
            return f"Good Signal Strenght - {val} dbm"
        if -70 <= val <= -61:
            return f"Moderate Signal Strenght - {val} dbm"
        if -80 <= val <= -71:
            return f"Bad Signal Strength - {val} dbm"
        return f"Poor Signal Strength - {val} dbm"
       
