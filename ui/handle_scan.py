import serial

from logger import setup_logger
from logic.NetScanner import NetScanner
from ui.clean_screen import clean_screen
from ui.logo import show_banner


def handle_scan() -> None:

    logger = setup_logger("FlipMarauder.Scan")

    clean_screen()
    show_banner()

    port = input("\nPaste the Port Name: ")
    logger.info("Scan requested for port: %s", port)

    scanner = NetScanner(port)

    print("Flipper: GPIO → USB-UART Bridge → Turn the Bridge On")
    print("\nPress Ctrl+C to stop scanning.\n")
    input("Press Enter When Bridge is Active...")
    logger.info("Starting scan loop")

    try:
        for network in scanner.start_scan():
            logger.info(
                "New network: ssid=%s bssid=%s ch=%s rssi=%s enc=%s",
                network.ssid,
                network.bssid,
                network.channel,
                network.rssi,
                network.encryption,
            )
            print(
                f"[NEW] SSID: {network.ssid} | BSSID: {network.bssid} | "
                f"CH: {network.channel} | RSSI: {network.rssi} | ENC: {network.encryption}"
            )

    except KeyboardInterrupt:
        scanner.stop_scan()
        logger.info("Scan stopped by user")
        print("\nScan stopped by user.")

    except serial.SerialException as exception:
        scanner.stop_scan()
        logger.exception("Serial error while scanning")
        print(f"Port Error: {exception}")

    except Exception as exception:
        scanner.stop_scan()
        logger.exception("Unexpected error while scanning")
        print(f"Error: {exception}")
