import os
import constants
import consigliere
import time


def symlink():
    mafia_library = os.path.join(constants.USER_ROOT, "Library", "Application Support", "KoLmafia", "")
    symlink_folder = os.path.join(constants.MAFIA_FOLDER, "Mafia Files")

    if os.path.isdir(mafia_library):
        if os.path.islink(symlink_folder):
            time.sleep(1)
            print(f"\n{constants.bcolors.FAIL}Symlink already exists{constants.bcolors.ENDC}\n\n")
        else:
            print(f"{constants.bcolors.OKGREEN}Creating symlink...{constants.bcolors.ENDC}")
            os.symlink(mafia_library, symlink_folder)
            print("Done.")


def chmod():
    print(constants.JAR_FILE_NAME)
    os.chmod(os.path.join(constants.MAFIA_FOLDER, constants.JAR_FILE_NAME), 0o755)


def main():
    print("\n################################")
    print("####      Mac    Patch      ####")
    print("################################\n")

    if constants.OPERATING_SYSTEM != "macOS":
        time.sleep(0.3)
        print(f"This patch is NOT meant to be run on {constants.OPERATING_SYSTEM} computers,\n"
              f"returning to the main menu.\n\n")
        time.sleep(5)
        consigliere.main()

    constants.CONFIG.read(constants.CONFIG_FILE)

    while True:
        print("The MacOS patch can be used to create a symlink between: \n\n"
              "     a) the Mafia files in the Application Support folder \n"
              "     b) the location of the Jar file "
              "This is helpful for accessing script files and user logs.")

        print("\nIt can also make an existing Jar file executable")

        print("\nMenu:")
        print(f"1: Create symlink")
        print(f"2: Make Jar executable")
        print(f"3: Run both")
        print(f"0: Return to the main menu\n")

        choice = input("Select: ")
        match choice:
            case "1":
                symlink()
            case "2":
                chmod()
            case "3":
                symlink()
                chmod()
            case "0":
                consigliere.main()
            case "_":
                print(f"\n{constants.bcolors.FAIL}Invalid choice. Please try again.{constants.bcolors.ENDC}\n\n")


if __name__ == "__main__":
    main()
