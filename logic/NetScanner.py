import time

import serial

from models.DataBaseManager import DataBaseManager
from models.marauder_parser import parse_line
from models.NetworkManager import NetworkManager


class NetScanner:
    def __init__(self, port: str, baudrate: int = 115200, logger=None):
        self.port = port
        self.baudrate = baudrate
        self.manager = NetworkManager()
        self.db = DataBaseManager()
        self.is_running = False
        self.logger = logger

    def start_scan(self):
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            self.is_running = True
            if self.logger:
                self.logger.info(
                    "Serial connected: port=%s baudrate=%s", self.port, self.baudrate
                )
            ser.write(b"scanap\r\n")
            if self.logger:
                self.logger.info("scanap command sent, waiting for AP data")

            last_no_data_log = time.monotonic()

            while self.is_running:
                if ser.in_waiting <= 0:
                    now = time.monotonic()
                    if self.logger and now - last_no_data_log >= 5:
                        self.logger.debug("No serial data received yet from Marauder")
                        last_no_data_log = now
                    time.sleep(0.05)
                    continue

                raw_line = ser.readline().decode("utf-8", errors="ignore").strip()
                if not raw_line:
                    continue

                wifi_network = parse_line(raw_line)
                if not wifi_network:
                    if self.logger:
                        self.logger.debug("Unparsed serial line: %s", raw_line)
                    continue

                network, is_new = self.manager.register_network(wifi_network)
                self.db.save_network(network_obj=wifi_network)

                if is_new:
                    yield network

    def stop_scan(self):
        self.is_running = False
        self.db.close()
