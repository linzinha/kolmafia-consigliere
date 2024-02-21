import mac_patch
import setup
import sys
import updater
import os

CONFIG_FILE_PATH = "config.ini"


def main_menu():
    print("╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭╮")
    print("┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃┃")
    print("┃┃╱╰╋━━┳━╮╭━━┳┳━━┫┃╭┳━━┳━┳━━╮")
    print("┃┃╱╭┫╭╮┃╭╮┫━━╋┫╭╮┃┃┣┫┃━┫╭┫┃━┫")
    print("┃╰━╯┃╰╯┃┃┃┣━━┃┃╰╯┃╰┫┃┃━┫┃┃┃━┫")
    print("╰━━━┻━━┻╯╰┻━━┻┻━╮┣━┻┻━━┻╯╰━━╯")
    print("╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃")
    print("╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯")

    print("\n Consigliere is a tool for updating your KoLmafia jar file, optimized for MacOS")
    while True:
        print("\nMenu:")
        print(f"1: Run the setup script")
        print(f"2: Update Mafia")
        print(f"3: Run MacOS Patch fix")
        print("0: Exit\n")

        choice = input("Select: ")
        match choice:
            case "1":
                os.system(f'python {setup.__file__}')
                sys.exit("Goodbye!")
            case "2":
                os.system(f'python {updater.__file__}')
                sys.exit("Goodbye!")
            case "3":
                os.system(f'python {mac_patch.__file__}')
            case "0":
                sys.exit("Goodbye!")
            case "_":
                print("Invalid choice. Please try again.")


def main():
    while True:
        main_menu()


if __name__ == "__main__":
    main()
