import time

import serial

from models.DataBaseManager import DataBaseManager
from models.marauder_parser import parse_line
from models.NetworkManager import NetworkManager


class NetScanner:
    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.manager = NetworkManager()
        self.db = DataBaseManager()
        self.is_running = False

    def start_scan(self):
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            self.is_running = True
            ser.write(b"scanap\r\n")

            while self.is_running:
                if ser.in_waiting <= 0:
                    time.sleep(0.05)
                    continue

                raw_line = ser.readline().decode("utf-8", errors="ignore").strip()
                if not raw_line:
                    continue

                wifi_network = parse_line(raw_line)
                if not wifi_network:
                    continue

                network, is_new = self.manager.register_network(wifi_network)
                self.db.save_network(network_obj=wifi_network)

                if is_new:
                    yield network

    def stop_scan(self):
        self.is_running = False
