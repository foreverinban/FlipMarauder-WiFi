import time

import serial

from models.DataBaseManager import DataBaseManager
from models.marauder_parser import parse_line
from models.NetworkManager import NetworkManager


class NetScanner:
    _NO_DATA_LOG_EVERY_SECONDS = 5
    _SCAN_RETRY_AFTER_IDLE_SECONDS = 15

    def __init__(self, port: str, baudrate: int = 115200, logger=None):
        self.port = port
        self.baudrate = baudrate
        self.manager = NetworkManager()
        self.is_running = False
        self.logger = logger
        self.db: DataBaseManager | None = None
        self.total_serial_lines = 0
        self.parsed_network_lines = 0

    def start_scan(self):
        self.db = DataBaseManager()
        self.total_serial_lines = 0
        self.parsed_network_lines = 0
        self.is_running = True
        try:
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                if not self.is_running:
                    return
                if self.logger:
                    self.logger.info(
                        "Serial connected: port=%s baudrate=%s", self.port, self.baudrate
                    )
                ser.write(b"scanap\r\n")
                if self.logger:
                    self.logger.info("scanap command sent, waiting for AP data")

                last_no_data_log = time.monotonic()
                last_data_at = last_no_data_log
                last_scan_retry_at = last_no_data_log

                while self.is_running:
                    if ser.in_waiting <= 0:
                        now = time.monotonic()
                        if self.logger and now - last_no_data_log >= self._NO_DATA_LOG_EVERY_SECONDS:
                            self.logger.debug("No serial data received yet from Marauder")
                            last_no_data_log = now
                        if (
                            now - last_data_at >= self._SCAN_RETRY_AFTER_IDLE_SECONDS
                            and now - last_scan_retry_at >= self._SCAN_RETRY_AFTER_IDLE_SECONDS
                        ):
                            ser.write(b"scanap\r\n")
                            last_scan_retry_at = now
                            if self.logger:
                                self.logger.warning(
                                    "No serial data for %ss, re-sent scanap command",
                                    self._SCAN_RETRY_AFTER_IDLE_SECONDS,
                                )
                        time.sleep(0.05)
                        continue

                    raw_line = ser.readline().decode("utf-8", errors="ignore").strip()
                    if not raw_line:
                        continue

                    last_data_at = time.monotonic()
                    self.total_serial_lines += 1
                    wifi_network = parse_line(raw_line)
                    if not wifi_network:
                        if self.logger:
                            self.logger.debug("Unparsed serial line: %s", raw_line)
                        continue

                    self.parsed_network_lines += 1
                    network, is_new = self.manager.register_network(wifi_network)
                    self.db.save_network(network_obj=network)

                    if is_new:
                        yield network
        finally:
            self.is_running = False
            if self.db is not None:
                self.db.close()
                self.db = None

    def stop_scan(self):
        self.is_running = False
