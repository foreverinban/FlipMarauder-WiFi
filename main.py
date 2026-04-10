import time

import serial

from models.DataBaseManager import DataBaseManager
from models.MarauderParser import MarauderParser
from models.NetworkManager import NetworkManager

manager = NetworkManager()
parser = MarauderParser()
db = DataBaseManager()

# Укажи свой порт
PORT = "/dev/cu.usbmodemflip_Anp4rut1"

try:
    # Добавляем timeout, чтобы readline() не зависал вечно
    with serial.Serial(PORT, 115200, timeout=1) as ser:
        print("🔧 Подготовка Flipper...")

        ser.write(b"loader close\r\n")
        time.sleep(1)
        ser.reset_input_buffer()
        
        print("🚀 Активирую Serial Bridge к ESP32...")
        ser.write(b"gpio serial_bridge 115200 13 14\r\n")
        time.sleep(2)
        
        ser.read_all()

        print("📦 Запрашиваю список команд у чипа...")
        ser.write(b"help\r\n")
        time.sleep(2)
        try:
            while True:
                if ser.in_waiting > 0:
                    raw_line = ser.readline().decode("utf-8", errors="ignore").strip()

                    # Пропускаем системные сообщения Флиппера, если они проскочат
                    if not raw_line or ">:" in raw_line:
                        continue

                    print(f"MARAUDER DATA: '{raw_line}'")

                    current_parsed_line = parser.parse_line(raw_line)

                    if current_parsed_line:
                        # Убедись, что в MarauderParser.py возвращается объект с полем .network
                        network_obj = manager.register_network(current_parsed_line)
                        db.save_network(network_obj=network_obj)
                        print(f"✅ Найдена сеть: {current_parsed_line}")

        except KeyboardInterrupt:
            print("\n⏹ Остановка пользователем...")
            manager.show_discovered_networks()

        finally:
            print("\nВыход из режима сканирования...")
            # В Marauder 'stopscan' или Ctrl+C (через мост может не работать, пробуем 'stop')
            ser.write(b"stop\r\n")
            time.sleep(0.5)
            # Чтобы выйти из режима bridge во Флиппере, нужно отправить специальный символ
            # или просто закрыть порт (что мы и делаем через with)

except serial.SerialException as e:
    print(f"❌ Ошибка порта: {e}")
except Exception as e:
    print(f"💥 Произошла ошибка: {e}")
