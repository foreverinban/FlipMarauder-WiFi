import math


class WiFiNetwork:
    def __init__(self, SSID, BSSID, RSSI, Channel, Encryption):
        self._SSID = SSID
        self._BSSID = BSSID
        self._Channel = Channel
        self._RSSI = RSSI
        self._Encryption = Encryption

    def __str__(self):
        return f"Network (SSID): {self._SSID}, Address (BSSID): {self._BSSID}, Channel: {self._Channel}, Signal Strength (RSSI): {self._RSSI}, Encryption type: {self._Encryption}"

    def __repr__(self):
        return f"WiFiNetwork(SSID:{self._SSID}, BSSID:{self._BSSID}, Channel:{self._Channel}, RSSI:{self._RSSI}, Encryption:{self._Encryption})"

    @staticmethod
    def RSSI_Rate(RSSI) -> str:
        if not isinstance(RSSI, int):
            RSSI = math.ceil(RSSI)

        if RSSI >= -50:
            return f"Very Good Signal Strenght - {RSSI} dbm"
        elif -60 <= RSSI <= -51:
            return f"Good Signal Strenght - {RSSI} dbm"
        elif -70 <= RSSI <= -61:
            return f"Moderate Signal Strenght - {RSSI} dbm"
        elif -80 <= RSSI <= -71:
            return f"Bad Signal Strength - {RSSI} dbm"
        elif RSSI <= -81:
            return f"Poor Signal Strength - {RSSI} dbm"
        else:
            pass
            # TODO: unexpected error

    @property
    def get_BSSID(self) -> str:
        return self._BSSID

    @property
    def get_Channel(self) -> str:
        return self._Channel
