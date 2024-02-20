import configparser
import glob
import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# noinspection SpellCheckingInspection
CONFIG_FILE_PATH = "config.ini"


def set_config(config, section, option, value):
    config.set(section, option, value)
    with open(CONFIG_FILE_PATH, "w") as config_file:
        config.write(config_file)
        print(f"Section {section}, option {option}, value {value}")


# Check current jar files count
def get_jar_count(config):
    mafia_folder = config.get('MAFIA_BUILD', 'mafia_folder', fallback=None)
    os.chdir(mafia_folder)
    jar_file_count = 0
    for file in glob.glob('*.jar'):
        jar_file_count += 1
    return jar_file_count


def get_jar_version(mafia_folder):
    script_directory = os.getcwd()
    os.chdir(mafia_folder)
    for file in glob.glob('*.jar'):
        version = re.split('[-.]', file)
        return version[1]
    os.chdir(script_directory)


def fetch_web_version(config, kolmafia_build_url):
    config.set('DEFAULT', 'last_run', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        response = requests.get(kolmafia_build_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        exit(1)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_url = kolmafia_build_url + next(link['href'] for link in soup.find_all('a', href=True) if
                                             link['href'].endswith('.jar'))
    version = re.split('[-.]', download_url)[-2:-1][0]
    # print(version)
    return download_url, version


def purge_duplicates(mafia_folder):
    script_directory = os.getcwd()
    os.chdir(mafia_folder)
    list_of_files = glob.glob('*.jar')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    for file in list_of_files:
        if file != latest_file:
            os.remove(file)
    os.chdir(script_directory)


def download_file(download_url, mafia_folder):
    new_jar_file = os.path.join(mafia_folder, os.path.basename(download_url))
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise an exception for any HTTP error
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        exit(1)
    with open(new_jar_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return new_jar_file


def main():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    mafia_folder = config.get('MAFIA_BUILD', 'mafia_folder', fallback=None)
    kolmafia_build_url = config.get('MAFIA_BUILD', 'kolmafia_build_url', fallback=None)
    jar_version_folder = get_jar_version(mafia_folder)
    download_url, jar_version_web = fetch_web_version(config, kolmafia_build_url)
    if jar_version_folder == jar_version_web:
        print("Latest version of Mafia is already installed")
        return
    else:
        print(f"Updating version of Mafia to {jar_version_web}")
        new_jar_file = download_file(download_url, mafia_folder)
        os.chmod(new_jar_file, 0o755)
        set_config(config, 'MAFIA_BUILD', 'jar_version', jar_version_web)
    jar_file_count = get_jar_count(config)
    if jar_file_count > 1:
        purge_duplicates(mafia_folder)
    jar_version_config_file = config.get('MAFIA_BUILD', 'jar_version', fallback=None)
    if jar_version_config_file == jar_version_folder and jar_version_web == jar_version_config_file:
        print("Latest version of Mafia is installed")
        return


if __name__ == "__main__":
    main()
