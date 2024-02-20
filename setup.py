import configparser
import os
import platform
import sys
import updater

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


def set_config(config, section, option, value):
    config.set(section, option, value)
    with open(CONFIG_FILE_PATH, "w") as config_file:
        config.write(config_file)
        option = str(option).replace('_', ' ')
        print(f"{option}: {value}")


def set_destination_folder(config):
    user_root = os.path.join(config['DEFAULT']['user_root'], '')
    print(user_root)
    while True:
        # noinspection SpellCheckingInspection
        input_location = input(f"\nEnter the destination folder path (or c to [c]ancel)\n"
                               f"--------------\n"
                               f"Set New Destination Folder Path: {user_root}").strip()
        if input_location.lower() not in RESPONSE_OPTIONS['CANCEL_OPTIONS']:
            mafia_folder = os.path.join(user_root, input_location)
            # noinspection SpellCheckingInspection
            verify_input = input(f"\nYou entered {mafia_folder}, is this correct? ([y]es/[n]o/[c]ancel): ")
            if not os.path.exists(mafia_folder):
                # noinspection SpellCheckingInspection
                verify_path = input(
                    f"{mafia_folder} is an Invalid folder path.\n"
                    f"Do you want to create this directory? ([y]es/[n]o/[c]ancel): ")
                if verify_path.lower() in RESPONSE_OPTIONS['YES_OPTIONS']:
                    os.makedirs(mafia_folder)
                else:
                    set_destination_folder(config)
            if verify_input in RESPONSE_OPTIONS['YES_OPTIONS'] and os.path.exists(mafia_folder):
                set_config(config, 'MAFIA_BUILD', 'mafia_folder', mafia_folder)
                return
        else:
            return


def main_menu(config, mafia_folder):
    while True:
        # Fetch the destination folder from the configuration
        print("\nMenu:")
        print(f"1: Set destination folder [CURRENTLY {mafia_folder}]")
        print(f"2: Run updater")
        print("0: Exit\n")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                mafia_folder = set_destination_folder(config)
            case "2":
                updater.main()
            case "0":
                sys.exit()
            case "_":
                print("Invalid choice. Please try again.")


def create_config_file():
    config['DEFAULT'] = DEFAULT
    config['MAFIA_BUILD'] = MAFIA_BUILD
    with open(CONFIG_FILE_PATH, 'x') as config_file:
        config.write(config_file)

def main():
    print(OPERATING_SYSTEM)
    # check if config file exists and create it if not
    config_file_exists = os.path.isfile(os.path.join(os.getcwd(), "config.ini"))
    if not config_file_exists:
        create_config_file()
    # check if configuration has been run, run if false
    for section in CONFIG_FILE_SECTIONS:
        if section in config.sections():
            continue
        else:
            print(f"Config file is missing {section}")
    config.read(CONFIG_FILE_PATH)
    mafia_folder = config['MAFIA_BUILD']['mafia_folder']
    if not mafia_folder:
        set_destination_folder(config)

    main_menu(config, mafia_folder)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    main()
