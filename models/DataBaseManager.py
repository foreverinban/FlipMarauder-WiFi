import sqlite3
from datetime import datetime


class DataBaseManager:
    def __init__(self, db_path="marauder_data.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
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

    def save_network(self, network_obj):
        now = datetime.now()

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO networks (bssid, ssid, encryption, channel, last_rssi, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                network_obj.bssid,
                network_obj.ssid,
                network_obj.encryption,
                network_obj.channel,
                network_obj.rssi,
                now,  # Используем нашу переменную с временем
            ),
        )

        self.cursor.execute(
            """
            INSERT INTO history (bssid, rssi, timestamp)
            VALUES (?, ?, ?)
            """,
            (network_obj.bssid, network_obj.rssi, now),  # И здесь тоже
        )

        self.conn.commit()
