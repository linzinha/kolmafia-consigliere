import re
import os
import requests
from bs4 import BeautifulSoup
import configparser
from datetime import datetime
import glob


def get_version_from_filename(filename):
    match = re.search(r'-(\d+)\.jar', filename)
    return match.group(1) if match else None


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


def purge_duplicates(folder):
    list_of_files = glob.glob(os.path.join(folder, '*.jar'))
    latest_file = max(list_of_files, key=os.path.getctime)
    for file in list_of_files:
        if file != latest_file:
            os.remove(file)


def download_and_update(config, web_version, mafia_folder, kolmafia_build_url):
    download_url, _ = fetch_web_version(kolmafia_build_url)
    new_jar_file = download_file(download_url, mafia_folder)
    os.chmod(new_jar_file, 0o755)

    # Update the config settings
    config.set('MAFIA_BUILD', 'jar_version', str(web_version))
    config.set('MAFIA_BUILD', 'last_updated', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("Downloaded and updated to the latest version.")
    purge_duplicates(mafia_folder)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    mafia_folder = config.get('MAFIA_BUILD', 'mafia_folder', fallback=None)
    kolmafia_build_url = config.get('MAFIA_BUILD', 'kolmafia_build_url', fallback=None)
    web_url = kolmafia_build_url
    web_version = fetch_web_version(web_url)[1]

    try:
        # Attempt to find the latest JAR file
        local_filename = max(glob.glob(os.path.join(mafia_folder, '*.jar')), key=os.path.getctime)
        local_version = get_version_from_filename(local_filename)
        config.set('MAFIA_BUILD', 'last_run', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    except ValueError:
        print("No JAR file found in the specified folder. Downloading a new one...")
        download_and_update(config, web_version, mafia_folder, kolmafia_build_url)
        return


    if local_version != web_version:
        print(f"Updating version of Mafia to {web_version}")
        download_and_update(config, web_version, mafia_folder, kolmafia_build_url)
    else:
        print("Latest version of Mafia is already installed.")

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    main()
