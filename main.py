import time
import serial

from models.DataBaseManager import DataBaseManager
from models.MarauderParser import MarauderParser
from models.NetworkManager import NetworkManager

manager = NetworkManager()
parser = MarauderParser()
db = DataBaseManager()


PORT = "/dev/cu.usbmodemflip_Anp4rut1"

print("Manual:")
print("   1. Flipper: GPIO → USB-UART Bridge → Turn the Bridge On")
print("   2. After the Activation the Port May Change — Check It Using scanner.py")
input("   3. Press Enter When Bridge is Active...")

try:
    with serial.Serial(PORT, 115200, timeout=1) as ser:
        print(f"Connected: {PORT}")
        ser.reset_input_buffer()

        print("Scanning is started")
        ser.write(b"scanap\r\n")
        time.sleep(1)

        try:
            while True:
                if ser.in_waiting > 0:
                    raw_line = ser.readline().decode("utf-8", errors="ignore").strip()

                    if not raw_line:
                        continue

                    print(f"RAW: '{raw_line}'")

                    wifi_network = parser.parse_line(raw_line)

                    if wifi_network:
                        manager.register_network(wifi_network)
                        db.save_network(network_obj=wifi_network)
                        signal = wifi_network.RSSI_Rate(wifi_network._RSSI)
                        print(f"Network is found: {wifi_network} | {signal}")

        except KeyboardInterrupt:
            print("\n Stopped by User...")
            ser.write(b"stopscan\r\n")
            time.sleep(0.5)
            manager.show_discovered_networks()

except serial.SerialException as e:
    print(f"Port Error: {e}")
except Exception as e:
    print(f"Error: {e}")
