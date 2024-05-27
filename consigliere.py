import mac_patch
import configure
import sys
import updater
import constants

CONFIG_FILE_PATH = "config.ini"


def main_menu():
    print("╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮")
    print("┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃")
    print("┃┃ ╰╋━━┳━━━╮╭━━┳┳━━┫┃╭┳━━━┳━━┳━━━╮")
    print("┃┃ ╭┫╭╮┃ ╭╮ ┫━━╋┫╭╮┃┃┣┫ ┃━┫╭━┫ ┃━┫")
    print("┃╰━╯┃╰╯┃ ┃┃ ┣━━┃┃╰╯┃╰┫┃ ┃━┫┃ ┃ ┃━┫")
    print("╰━━━┻━━┻━╯╰━┻━━┻┻━╮┣━┻┻━━━┻╯ ╰━━━╯")
    print("╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃")
    print("╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯")

    print("\n Consigliere is a tool for updating your KoLmafia jar file, optimized for MacOS")
    constants.CONFIG.read(constants.CONFIG_FILE)

    while True:
        print("\nMenu:")
        print(f"1: Run the setup script")
        print(f"2: Update Mafia")
        print(f"3: Run MacOS Patch fix")
        print("0: Exit\n")

        choice = input("Select: ")
        match choice:
            case "1":
                configure.main()
            case "2":
                updater.main()
            case "3":
                mac_patch.main()
            case "0":
                sys.exit("Goodbye!")
            case "_":
                print(f"\n{constants.bcolors.FAIL}Invalid choice. Please try again.{constants.bcolors.ENDC}\n\n")


def main():
    while True:
        main_menu()


if __name__ == "__main__":
    print(sys.version[0:4])

    main()
