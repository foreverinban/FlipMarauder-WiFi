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
    def rssi_rate(self) -> str:
        val = math.ceil(self.rssi)

        if self.rssi >= -50:
            return f"Very Good Signal Strength - {val} dbm"
        if -60 <= self.rssi <= -51:
            return f"Good Signal Strength - {val} dbm"
        if -70 <= self.rssi <= -61:
            return f"Moderate Signal Strength - {val} dbm"
        if -80 <= self.rssi <= -71:
            return f"Bad Signal Strength - {val} dbm"
        return f"Poor Signal Strength - {val} dbm"
       
