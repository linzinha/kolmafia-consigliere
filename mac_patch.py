import configparser
import os
import shutil
import sys

import consigliere


def symlink():
    mafia_library = os.path.join(USER_ROOT, "Library", "Application Support", "KoLmafia", "")
    if os.path.isdir(mafia_library):
        if os.path.islink(mafia_folder):
            print("Symlink already exists")
        else:
            list_files = os.listdir(mafia_folder)
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
            os.rename(mafia_folder, temp_mafia_folder)
            print("Done. Creating symlink...")
            os.symlink(mafia_library, mafia_folder)
            print("Done. Moving jar file into the symlink folder...")
            os.rename(os.path.join(temp_mafia_folder, jar_file_name), os.path.join(mafia_folder, jar_file_name))
            print("Done. Removing temporary directory...")
            shutil.rmtree(temp_mafia_folder)
            print("Done.")


def chmod():
    print(jar_file_name)
    os.chmod(os.path.join(mafia_folder, jar_file_name), 0o755)


def main():
    print("\n################################")
    print("####      Mac    Patch      ####")
    print("################################\n")
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
                quit()
            case "_":
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    CONFIG_FILE_PATH = "config.ini"
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    USER_ROOT = os.path.expanduser("~")  # Starting path for the script execution
    mafia_folder = config.get('MAFIA_BUILD', 'mafia_folder', fallback=None)
    temp_mafia_folder = f"{mafia_folder}_tmp"
    jar_version = config.get('MAFIA_BUILD', 'jar_version', fallback=None)
    jar_file_name = f"KoLmafia-{jar_version}.jar"
    main()
