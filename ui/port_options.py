import time

from logic.port_scanner import check_ports


def port_options() -> str | None:
    available_ports = check_ports()

    for key, value in available_ports.items():
        print(f"{key} : {value}")

    print("\n")

    while True:
        try:
            chosen_port = int(input("Enter the chosen port number: "))
        except ValueError:
            print("Invalid input. Please enter a port number.")
            time.sleep(2)
            continue

        selected_port = available_ports.get(str(chosen_port))
        if selected_port is None:
            print("Port number not found. Try again.")
            time.sleep(2)
            continue

        return selected_port
