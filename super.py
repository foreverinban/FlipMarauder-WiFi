import os
import time

from ui.logo import show_banner
from logic.net_scanner import scanning
from logic.port_scanner import check_ports

while True:
    
    os.system("cls" if os.name == "nt" else "clear")
    show_banner()

    print("Welcome to FlipMarauder!\n")
    print("Please Choose the Option:\n")
    print("  1 - List All Ports")
    print("  2 - Start Scanning (Requires Port)")
    print("  0 - Exit\n")

    try:
        option = int(input("Enter the Option: "))
    except ValueError:
        print("Invalid Input. Please Enter a Number.")
        time.sleep(2)
        continue

    if option == 1:
        os.system("cls" if os.name == "nt" else "clear")
        print(check_ports())
        input("\nPress Enter to Return to the Menu...")

    elif option == 2:
        os.system("cls" if os.name == "nt" else "clear")
        port = input("\nPaste the Port Name: ")
        scanning(port)
        input("\nPress Enter to Return to the Menu...")

    elif option == 0:
        os.system("cls" if os.name == "nt" else "clear")
        print("Thank You for Using FlipMarauder!")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
        break

    else:
        print("This Option Does Not Exist. Please Enter 0, 1 or 2.")
        time.sleep(2)
