def show_discovered_networks(rows: list[dict]) -> None:
    print(f"\n{'SSID':<25} | {'BSSID':<18} | {'Hits':<5} | {'Signal'}")
    print("-" * 75)

    for row in rows:
        signal = f"{row['rssi']} dBm"
        print(f"{row['ssid']:<25} | {row['bssid']:<18} | {row['hits']:<5} | {signal}")

