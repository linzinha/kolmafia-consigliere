import mac_patch
import setup
import sys
import updater

CONFIG_FILE_PATH = "config.ini"


def main_menu():
    while True:
        print("╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭╮")
        print("┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃┃")
        print("┃┃╱╰╋━━┳━╮╭━━┳┳━━┫┃╭┳━━┳━┳━━╮")
        print("┃┃╱╭┫╭╮┃╭╮┫━━╋┫╭╮┃┃┣┫┃━┫╭┫┃━┫")
        print("┃╰━╯┃╰╯┃┃┃┣━━┃┃╰╯┃╰┫┃┃━┫┃┃┃━┫")
        print("╰━━━┻━━┻╯╰┻━━┻┻━╮┣━┻┻━━┻╯╰━━╯")
        print("╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃")
        print("╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯")

        print("\n Consigliere is a tool for updating your KoLmafia jar file, optimized for MacOS")

        print("\nMenu:")
        print(f"1: Run the setup script")
        print(f"2: Update Mafia")
        print(f"3: Run MacOS Patch fix")
        print("0: Exit\n")

        choice = input("Enter your choice: ")
        match choice:
            case "1":
                setup.main()
            case "2":
                updater.main()
            case "3":
                mac_patch.main()
            case "0":
                sys.exit()
            case "_":
                print("Invalid choice. Please try again.")


def main():
    while True:
        main_menu()


if __name__ == "__main__":
    main()
