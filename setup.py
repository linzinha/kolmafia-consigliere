import configparser
import os
import platform
import sys
import updater
import mac_patch

# Constants
CONFIG_FILE_PATH = 'config.ini'
CONFIG_FILE_SECTIONS = ['MAFIA_BUILD']
OPERATING_SYSTEM = platform.platform().split('-')[0]
USER_ROOT = os.path.expanduser("~")  # Starting path for the script execution
KOLMAFIA_BUILD_URL = 'https://ci.kolmafia.us/job/Kolmafia/lastSuccessfulBuild/'
RESPONSE_OPTIONS = {'YES_OPTIONS': ['y', 'yes'], 'NO_OPTIONS': ['n', 'no'], 'CANCEL_OPTIONS': ['c', 'cancel']}
DEFAULT = {
    'os': OPERATING_SYSTEM,
    'user_root': USER_ROOT
}

MAFIA_BUILD = {
    'kolmafia_build_url': KOLMAFIA_BUILD_URL,
    "mafia_folder": USER_ROOT,
    'last_run': '',
    'last_updated': '',
    'jar_version': '',
    'jar_hash': ''
}


def set_config(section, option, value):
    config.set(section, option, value)
    with open(CONFIG_FILE_PATH, "w") as config_file:
        config.write(config_file)
        option = str(option).replace('_', ' ')
        print(f"{option}: {value}")


def verify_response(response):
    if response in RESPONSE_OPTIONS['YES_OPTIONS']:
        return True
    if response in RESPONSE_OPTIONS['NO_OPTIONS']:
        set_destination_folder()
    if response in RESPONSE_OPTIONS['CANCEL_OPTIONS']:
        main()


def set_destination_folder():
    user_root = os.path.join(config['DEFAULT']['user_root'], '')
    while True:
        input_location = input(f"\nEnter the destination folder path (or c to [c]ancel)\n"
                               f"--------------\n"
                               f"Set New Destination Folder Path: {user_root}").strip()
        verify_response(input_location)
        mafia_folder = os.path.join(user_root, input_location)
        verify_input = input(f"\nYou entered {mafia_folder}, is this correct? ([y]es/[n]o/[c]ancel): ")
        test = verify_response(verify_input)
        print(test)
        if not os.path.exists(mafia_folder):
            verify_path = input(
                f"{mafia_folder} is an Invalid folder path.\n"
                f"Do you want to create this directory? ([y]es/[n]o/[c]ancel): ")
            verify_response(verify_path)
            os.makedirs(mafia_folder)
            set_config('MAFIA_BUILD', 'mafia_folder', mafia_folder)
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
                os.system(f'python {updater.__file__}')
            case "3":
                os.system(f'python {mac_patch.__file__}')
            case "0":
                quit()
            case "_":
                print("Invalid choice. Please try again.")


def create_config_file():
    config['DEFAULT'] = DEFAULT
    config['MAFIA_BUILD'] = MAFIA_BUILD
    with open(CONFIG_FILE_PATH, 'x') as config_file:
        config.write(config_file)


def main():
    # check if config file exists and create it if not
    config_file_exists = os.path.isfile(os.path.join(os.getcwd(), "config.ini"))
    if not config_file_exists:
        create_config_file()
    # check if configuration has been run, run if false
    for section in CONFIG_FILE_SECTIONS:
        print(f"Section: {section}")
        if section in config.sections():
            continue
        else:
            print(f"Config file is missing {section}")
    config.read(CONFIG_FILE_PATH)
    mafia_folder = config['MAFIA_BUILD']['mafia_folder']
    if not mafia_folder:
        set_destination_folder()

    main_menu(mafia_folder)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    main()
