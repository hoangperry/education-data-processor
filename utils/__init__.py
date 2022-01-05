import os
import urllib.parse
import requests


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def duckduckgo_api(university_name):
    duckduckgo_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(university_name)}&format=json&pretty=1"
    res = requests.get(duckduckgo_url)
    return res.json(), duckduckgo_url
