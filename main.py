import os
import time


from ui.logo import show_banner
from logic.port_scanner import check_ports
from ui.handle_scan import handle_scan

def clean_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main_menu() -> None:
    while True:
        
        clean_screen()
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
            clean_screen()
            show_banner()
            print(check_ports())
            input("\nPress Enter to Return to the Menu...")

        elif option == 2:
            handle_scan()
            input("\nPress Enter to Return to the Menu...")

        elif option == 0:
            clean_screen()

            print("Thank You for Using FlipMarauder!")

            time.sleep(2)
            clean_screen()
            break

        else:
            print("This Option Does Not Exist. Please Enter 0, 1 or 2.")
            time.sleep(2)

if __name__ == "__main__":
    main_menu()
