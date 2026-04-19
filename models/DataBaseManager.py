import sqlite3
from datetime import datetime
from models.WiFiNetwork import WiFiNetwork


class DataBaseManager:
    _COMMIT_EVERY = 20  # flush to disk every N writes

    def __init__(self, db_path="marauder_data.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.cursor = self.conn.cursor()
        self._pending = 0
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS networks (
                bssid TEXT PRIMARY KEY,
                ssid TEXT,
                encryption TEXT,
                channel INTEGER,
                last_rssi INTEGER,
                last_seen DATETIME
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT,
                rssi INTEGER,
                timestamp DATETIME,
                FOREIGN KEY (bssid) REFERENCES networks (bssid)
            )
        """)
        self.conn.commit()

    def save_network(self, network_obj: WiFiNetwork) -> None:
        now = datetime.now()
        self.cursor.execute(
            """
            INSERT INTO networks (bssid, ssid, encryption, channel, last_rssi, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(bssid) DO UPDATE SET
                ssid=excluded.ssid,
                encryption=excluded.encryption,
                channel=excluded.channel,
                last_rssi=excluded.last_rssi,
                last_seen=excluded.last_seen
            """,
            (network_obj.bssid, network_obj.ssid, network_obj.encryption,
             network_obj.channel, network_obj.rssi, now),
        )
        self.cursor.execute(
            "INSERT INTO history (bssid, rssi, timestamp) VALUES (?, ?, ?)",
            (network_obj.bssid, network_obj.rssi, now),
        )
        self._pending += 1
        if self._pending >= self._COMMIT_EVERY:
            self.flush()

    def flush(self):
        if self._pending:
            self.conn.commit()
            self._pending = 0

    def close(self):
        self.flush()
        self.conn.close()
