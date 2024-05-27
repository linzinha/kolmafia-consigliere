import configparser
import platform
import os

CONFIG = configparser.ConfigParser()
CONFIG_FILE = 'config.ini'
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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CONFIG.read(CONFIG_FILE)
MAFIA_FOLDER = CONFIG.get('MAFIA_BUILD', 'mafia_folder', fallback=None)
TEMP_MAFIA_FOLDER = f"{MAFIA_FOLDER}_tmp"
JAR_VERSION = CONFIG.get('MAFIA_BUILD', 'jar_version', fallback=None)
JAR_FILE_NAME = f"KoLmafia-{JAR_VERSION}.jar"