import os
import updater
import mac_patch
import constants
import sys


def set_config(section, option, value):
    constants.CONFIG.set(section, option, value)
    with open(constants.CONFIG_FILE, "w") as config_file:
        constants.CONFIG.write(config_file)
        option = str(option).replace('_', ' ')
        print(f"{option}: {value}")


def verify_response(response):
    if response in constants.RESPONSE_OPTIONS['YES_OPTIONS']:
        return True
    if response in constants.RESPONSE_OPTIONS['NO_OPTIONS']:
        set_destination_folder()
    if response in constants.RESPONSE_OPTIONS['CANCEL_OPTIONS']:
        main()


def set_destination_folder():
    user_root = os.path.join(constants.CONFIG['DEFAULT']['user_root'], '')
    while True:
        input_location = input(f"\nEnter the destination folder path (or c to [c]ancel)\n"
                               f"--------------\n"
                               f"Set New Destination Folder Path: {user_root}").strip()
        verify_response(input_location)
        mafia_folder = os.path.join(user_root, input_location)
        verify_input = input(f"\nYou entered {mafia_folder}, is this correct? ([y]es/[n]o/[c]ancel): ")
        if not os.path.exists(mafia_folder):
            verify_path = input(
                f"{mafia_folder} is an Invalid folder path.\n"
                f"Do you want to create this directory? ([y]es/[n]o/[c]ancel): ")
            verify_response(verify_path)
            os.makedirs(mafia_folder)
        set_config('MAFIA_BUILD', 'mafia_folder', mafia_folder)
        print("\nMafia folder has been set!\n")
        return mafia_folder


def main_menu(mafia_folder):
    print("\n#########################################")
    print("####      Installation    Setup      ####")
    print("#########################################\n")
    while True:
        # Fetch the destination folder from the configuration
        print("Menu:")
        print(f"1: Set destination folder [CURRENTLY {mafia_folder}]")
        print(f"2: Update Mafia")
        print(f"3: Run MacOS Patch fix")
        print(f"0: Exit\n")

        choice = input("Select: ")

        match choice:
            case "1":
                mafia_folder = set_destination_folder()
            case "2":
                updater.main()
            case "3":
                mac_patch.main()
            case "0":
                sys.exit("Goodbye!")
            case "_":
                print("Invalid choice. Please try again.")


def create_config_file():
    constants.CONFIG['DEFAULT'] = constants.DEFAULT
    constants.CONFIG['MAFIA_BUILD'] = constants.MAFIA_BUILD
    with open(constants.CONFIG_FILE, 'x') as config_file:
        constants.CONFIG.write(config_file)


def main():
    # check if config file exists and create it if not
    config_file_exists = os.path.isfile(os.path.join(os.getcwd(), "config.ini"))
    if not config_file_exists:
        create_config_file()
    # check if configuration has been run, run if false
    for section in constants.CONFIG_FILE_SECTIONS:
        if section in constants.CONFIG.sections():
            continue
        else:
            print(f"Config file is missing {section}")
    constants.CONFIG.read(constants.CONFIG_FILE)
    mafia_folder = constants.CONFIG['MAFIA_BUILD']['mafia_folder']
    if not mafia_folder:
        set_destination_folder()

    main_menu(mafia_folder)


if __name__ == "__main__":
    main()
