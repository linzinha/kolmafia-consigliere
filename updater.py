import re
import os
import requests
from datetime import datetime
import glob
import time
import constants
import mac_patch


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
    
    version = response.json()["name"]
    url = response.json()["assets"][1]["browser_download_url"]

    return url, version


# purge_duplicates is run every time regardless of whether a new file is downloaded
# this is done in case there are multiple versions for any reason
def purge_duplicates(folder):
    list_of_files = glob.glob(os.path.join(folder, '*.jar'))
    latest_file = max(list_of_files, key=os.path.getctime)
    for file in list_of_files:
        if file != latest_file:
            os.remove(file)


# Called by main if an update is needed
def download_and_update(mafia_folder, download_url, web_version):
    constants.CONFIG.read(constants.CONFIG_FILE)
    # defines the destination of the downloaded file, then tries to download it
    # raises an exception if the download request fails, if successful the download is chunked
    new_jar_file = os.path.join(mafia_folder, os.path.basename(download_url))
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error downloading file: {e}")

    with open(new_jar_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            _ = file.write(chunk) if chunk else None

    # Update the config file, is the function in configure.py really needed?
    constants.CONFIG.set('MAFIA_BUILD', constants.JAR_VERSION, str(web_version))
    constants.CONFIG.set('MAFIA_BUILD', 'last_updated', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # runs chmod if the script is run on a Mac, since Macs don't allow the jar files to be executable on download
    if constants.OPERATING_SYSTEM == "MacOS":
        mac_patch.chmod()

    time.sleep(2)
    print("Downloaded and updated to the latest version.\n\n")
    purge_duplicates(mafia_folder)
    # changes to the config file are written
    with open(constants.CONFIG_FILE, 'w') as configfile:
        constants.CONFIG.write(configfile)

    return new_jar_file


def main():
    # fetch the latest version from the website
    download_url, web_version = fetch_web_version(constants.KOLMAFIA_BUILD_URL)
    # Attempt to locate a local jar file for comparison, and if none is found,
    # go straight to downloading the latest version (updating last_run in the config file first)
    constants.CONFIG.set('MAFIA_BUILD', 'last_run', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    mafia_folder = constants.CONFIG.get('MAFIA_BUILD', 'mafia_folder', fallback=None)
    try:
        local_filename = max(glob.glob(os.path.join(mafia_folder, '*.jar')), key=os.path.getctime)
        local_version = get_version_from_filename(local_filename)
        time.sleep(0.3)
    except ValueError:
        print("\nNo JAR file found in the specified folder. Downloading a new one...")
        download_and_update(mafia_folder, download_url, web_version)
        return
    # If a jar file is found, but doesn't match what is found online, the file is updated
    # If the version numbers match however, the file is not downloaded
    if local_version != web_version:
        print(f"\nUpdating version of Mafia to {web_version}")
        download_and_update(mafia_folder, download_url, web_version)
    else:
        time.sleep(2)
        print("\nLatest version of Mafia is already installed.\n\n")
    # write all changes to the config file
    with open('config.ini', 'w') as configfile:
        constants.CONFIG.write(configfile)


if __name__ == "__main__":
    main()
