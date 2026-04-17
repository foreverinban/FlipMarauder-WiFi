import time

from ui.clean_screen import clean_screen
from ui.handle_scan import handle_scan
from ui.logo import show_banner


def main_menu() -> None:
    while True:
        clean_screen()
        show_banner()

        print("Welcome to FlipMarauder!\n")
        print("Please Choose the Option:\n")
        print("  1 - Choose Port & Start Scanning\n")
        print("  0 - Exit\n")

        try:
            option = int(input("Enter the Option: "))

        except ValueError:
            print("Invalid Input. Please Enter a Number.")
            time.sleep(2)
            continue

        if option == 1:
            handle_scan()
            input("\nPress Enter to Return to the Menu...")

        elif option == 0:
            clean_screen()

            print("Thank You for Using FlipMarauder!")

            time.sleep(2)
            clean_screen()
            break

        else:
            print("This Option Does Not Exist. Please Enter 0 or 1")
            time.sleep(2)


if __name__ == "__main__":
    main_menu()
