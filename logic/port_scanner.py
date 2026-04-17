import serial.tools.list_ports


def check_ports():
    ports = serial.tools.list_ports.comports()

    port_dict = {}

    for temp, port in enumerate(ports, start=1):
        port_dict[str(temp)] = port.device

    return port_dict
