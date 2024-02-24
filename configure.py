import os
import updater
import mac_patch
import constants
import sys


# at multiple points, set_destination_folder verifies user input
# at each point the result of the choice is the same, so verify_response is called to handle the response
def verify_response(response):
    if response in constants.RESPONSE_OPTIONS['YES_OPTIONS']:
        return True
    if response in constants.RESPONSE_OPTIONS['NO_OPTIONS']:
        set_destination_folder()
    if response in constants.RESPONSE_OPTIONS['CANCEL_OPTIONS']:
        main()


# interactive function where user identifies where their mafia .jar file should be
# user_root identifies the user's root/home folder, and the user is prompted to complete the path to their .jar file
# maybe make this a popup window for folder selection?
def set_destination_folder():
    user_root = os.path.join(constants.CONFIG['DEFAULT']['user_root'], '')
    while True:
        input_location = input(f"\nEnter the destination folder path (or c to [c]ancel)\n"
                               f"--------------\n"
                               f"Set New Destination Folder Path: {user_root}").strip()
        verify_response(input_location)
        mafia_folder = os.path.join(user_root, input_location)
        verify_input = input(f"\nYou entered {mafia_folder}, is this correct? ([y]es/[n]o/[c]ancel): ")
        verify_response(verify_input)
        if not os.path.exists(mafia_folder):  # ask user if they want to create the parent folder if it doesn't exist
            verify_path = input(
                f"{mafia_folder} is an Invalid folder path.\n"
                f"Do you want to create this directory? ([y]es/[n]o/[c]ancel): ")
            verify_response(verify_path)
            os.makedirs(mafia_folder)
        constants.CONFIG.set('MAFIA_BUILD', constants.MAFIA_FOLDER, mafia_folder)
        with open(constants.CONFIG_FILE, 'w') as configfile:
            constants.CONFIG.write(configfile)
        print("\nMafia folder has been set!\n")
        return mafia_folder


def main_menu(mafia_folder):
    print("\n#########################################")
    print("####      Installation    Setup      ####")
    print("#########################################\n")
    while True:
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


# if config.ini is missing in the script folder, this function is called to create one
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
            # TODO manage partial config files more gracefully/automatically
            print(f"Config file is missing {section}.\n"
                  f"Delete the existing config.ini in the consigliere script folder \n"
                  f"and rerun the configuration")
    constants.CONFIG.read(constants.CONFIG_FILE)
    mafia_folder = constants.CONFIG['MAFIA_BUILD']['mafia_folder']
    # forces set_destination_folder to run if mafia_folder is empty on the config file
    if not mafia_folder:
        set_destination_folder()

    main_menu(mafia_folder)


if __name__ == "__main__":
    main()
