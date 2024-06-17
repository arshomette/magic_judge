import os
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from urllib.error import HTTPError

""" This script attempts to download the latest Comprehensive Rules,
Tournament Rules, Infraction Guide, and the oracle database of unique cards.
The destination folder is {projecthome}/data"""

def download_file(base_url, file_pattern_regex, local_path):
    try:
        response = requests.get(base_url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        file_pattern = re.compile(file_pattern_regex)
        file_tags = soup.find_all('a', href=True)
        file_url = None
        for tag in file_tags:
            if file_pattern.search(tag['href']):
                file_url = tag['href'].replace(' ', '%20')
                break
        if file_url:
            urllib.request.urlretrieve(file_url, local_path)
            print(f"File downloaded successfully: {local_path}")
        else:
            print("No matching file found.")

    except HTTPError as e:
        print(f"HTTP Error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

update_files = {
    "MagicCompRules.txt": {
        "regex": r"MagicCompRules \d{8}\.txt",
        "url": "https://magic.wizards.com/en/rules"
    },
    "MTG_MTR.pdf": {
        "regex": r"MTG_MTR_.*\.pdf",
        "url": "https://wpn.wizards.com/en/rules-documents"
    },
    "MTG_IPG.pdf": {
        "regex": r"MTG_IPG_.*_EN\.pdf",
        "url": "https://wpn.wizards.com/en/rules-documents"
    },
    "oracle_cards.json": {
        "regex": r"oracle-cards-.*\.json",
        "url": "https://scryfall.com/docs/api/bulk-data"
    }
}

relative_path = os.path.join('data')

for key, value in update_files.items():
    base_url = value["url"]
    file_pattern_regex = value["regex"]
    local_path = os.path.join(relative_path, key)

    download_file(base_url, file_pattern_regex, local_path)

