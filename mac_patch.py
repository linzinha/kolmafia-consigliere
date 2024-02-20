import configparser
import os
import shutil

CONFIG_FILE_PATH = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
USER_ROOT = os.path.expanduser("~")  # Starting path for the script execution
mafia_folder = config.get('MAFIA_BUILD', 'mafia_folder', fallback=None)
jar_version = config.get('MAFIA_BUILD', 'jar_version', fallback=None)
jar_file_name = f"KoLmafia-{jar_version}.jar"
print(jar_version)
mafia_folder2 = f"{mafia_folder}_tmp"
print(mafia_folder2)
mafia_library = os.path.join(USER_ROOT, "Library", "Application Support", "KoLmafia", "")
if os.path.isdir(mafia_library):
    if os.path.islink(mafia_folder):
        print("Symlink already exists")
    else:
        os.rename(mafia_folder, mafia_folder2)
        os.symlink(mafia_library, mafia_folder)
        os.rename(os.path.join(mafia_folder2, jar_file_name), os.path.join(mafia_folder, jar_file_name))
        os.chmod(os.path.join(mafia_folder, jar_file_name), 0o755)
        shutil.rmtree(mafia_folder2)
