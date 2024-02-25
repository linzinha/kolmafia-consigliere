import os
import shutil
import constants
import consigliere
import time
constants.CONFIG.read(constants.CONFIG_FILE)


def symlink():
    mafia_library = os.path.join(constants.USER_ROOT, "Library", "Application Support", "KoLmafia", "")
    if os.path.isdir(mafia_library):
        if os.path.islink(constants.MAFIA_FOLDER):
            print("Symlink already exists")
        else:
            list_files = os.listdir(constants.MAFIA_FOLDER)
            if len(list_files) > 1:
                file_count = len(list_files) - 1
                print("found {} additional files in that location".format(file_count))
                for file in list_files:
                    if not file.endswith(".jar"):
                        print(file)
                confirm = input("Are you sure you want to continue? (y/n): ")
                if confirm != "y":
                    return
            print("Moving .jar folder to a temporary directory...")
            os.rename(constants.MAFIA_FOLDER, constants.TEMP_MAFIA_FOLDER)
            print("Done. Creating symlink...")
            os.symlink(mafia_library, constants.MAFIA_FOLDER)
            print("Done. Moving jar file into the symlink folder...")
            os.rename(os.path.join(constants.TEMP_MAFIA_FOLDER, constants.JAR_FILE_NAME),
                      os.path.join(constants.MAFIA_FOLDER, constants.JAR_FILE_NAME))
            print("Done. Removing temporary directory...")
            shutil.rmtree(constants.TEMP_MAFIA_FOLDER)
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
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
