import setup
import sys
import updater

CONFIG_FILE_PATH = "config.ini"


def main_menu():
    while True:
        # Fetch the destination folder from the configuration

        print("\nMenu:")
        print(f"1: Run the setup script")
        print(f"2: Update Mafia")
        print("0: Exit\n")

        choice = input("Enter your choice: ")
        match choice:
            case "1":
                setup.main()
            case "2":
                updater.main()
            case "0":
                sys.exit()
            case "_":
                print("Invalid choice. Please try again.")


def main():
    while True:
        main_menu()


if __name__ == "__main__":
    main()
