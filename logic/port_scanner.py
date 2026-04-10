import serial.tools.list_ports


def check_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Port: {port.device}, Description: {port.description}")


if __name__ == "__main__":
    check_ports()

#Port: /dev/cu.usbmodemflip_Anp4rut1, Description: Anp4rut