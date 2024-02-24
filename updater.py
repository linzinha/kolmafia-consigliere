import re
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import glob
import time
import constants


# identifies currently installed kolmafia version
def get_version_from_filename(filename):
    match = re.search(r'-(\d+)\.jar', filename)
    return match.group(1) if match else None


# identifies the latest build version number
def fetch_web_version(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching web version: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')
    download_url = url + next(link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.jar'))
    version = re.search(r'-(\d+)\.jar', download_url).group(1)
    return download_url, version


# download script, called if the version installed is out of date
def download_file(download_url, folder):
    new_jar_file = os.path.join(folder, os.path.basename(download_url))
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error downloading file: {e}")

    with open(new_jar_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            _ = file.write(chunk) if chunk else None
    return new_jar_file


# purge_duplicates is run every time regardless of whether a new file is downloaded
# this is done in case there are multiple versions for any reason
def purge_duplicates(folder):
    list_of_files = glob.glob(os.path.join(folder, '*.jar'))
    latest_file = max(list_of_files, key=os.path.getctime)
    for file in list_of_files:
        if file != latest_file:
            os.remove(file)


# Called by main if an update is needed
# main calls download_and_update, which calls download_file to actually perform the download
# download_and_update assembles the specific url for the new file but is currently inefficient
# todo remove the second call of fetch_web_version
# we should be able to pass it as an argument, or assemble the url in main
# download_and_update sets the jar_version and last_updated entries on the configf file
# it also runs chmod
# todo only run chmod if MacOS, maybe call mac patch script
# todo restructure and rename download_and_update and download_file scripts

def download_and_update(web_version, mafia_folder, kolmafia_build_url):
    download_url, _ = fetch_web_version(kolmafia_build_url)
    new_jar_file = download_file(download_url, mafia_folder)
    os.chmod(new_jar_file, 0o755)

    # Update the config settings
    constants.CONFIG.set('MAFIA_BUILD', 'jar_version', str(web_version))
    constants.CONFIG.set('MAFIA_BUILD', 'last_updated', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(2)
    print("Downloaded and updated to the latest version.\n\n")
    purge_duplicates(mafia_folder)
    with open(constants.CONFIG_FILE, 'w') as configfile:
        constants.CONFIG.write(configfile)


def main():
    # read the config file and fetch the latest version from the website
    web_version = fetch_web_version(constants.KOLMAFIA_BUILD_URL)[1]
    # Attempt to locate a local jar file for comparison, and if none is found,
    # go straight to downloading the latest version (updating last_run in the config file first)
    constants.CONFIG.set('MAFIA_BUILD', 'last_run', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        local_filename = max(glob.glob(os.path.join(constants.MAFIA_FOLDER, '*.jar')), key=os.path.getctime)
        local_version = get_version_from_filename(local_filename)
        time.sleep(0.3)
    except ValueError:
        print("\nNo JAR file found in the specified folder. Downloading a new one...")
        download_and_update(web_version, constants.MAFIA_FOLDER, constants.KOLMAFIA_BUILD_URL)
        return
    # If a jar file is found, but doesn't match what is found online, the file is updated
    # If the version numbers match however, the file is not downloaded
    if local_version != web_version:
        print(f"\nUpdating version of Mafia to {web_version}")
        download_and_update(web_version, constants.MAFIA_FOLDER, constants.KOLMAFIA_BUILD_URL)
    else:
        time.sleep(2)
        print("\nLatest version of Mafia is already installed.\n\n")
    # write all changes to the config file
    with open('config.ini', 'w') as configfile:
        constants.CONFIG.write(configfile)


if __name__ == "__main__":
    main()
