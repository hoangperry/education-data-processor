import re
import requests
import urllib.parse
import pandas as pd

from io import StringIO
from utils.environments import create_environments

env = create_environments()


def duckduckgo_api(university_name):
    # noinspection PyBroadException
    try:
        duckduckgo_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(university_name)}&format=json&pretty=1"
        res = requests.get(duckduckgo_url)
    except Exception as _:
        return dict(), ''
    return res.json(), duckduckgo_url


def parse_year_from_file_name(filename) -> int:
    """
    default filename partern data-<Year>.[csv|txt]
    :param filename:
    :return: year as integer
    """
    return int(re.search(r'\d+', filename).group())


# noinspection PyBroadException
def process_data(file_data) -> list:
    """
    Process file data as byte
        - Clean columns name: lower case, strip
        - Clean value: strip
    :param file_data: byte
    :return: list of university
    """
    data_file = pd.read_csv(StringIO(str(file_data, 'utf-8')), sep='\t')
    data_list = list()
    for _, row in data_file[1:].iterrows():
        new_dict = dict()
        for i in zip(data_file.columns, row):
            new_dict[re.sub(r'\s+', ' ', i[0].strip().lower())] = i[1]
        # Enrich data
        j_data, duck_url = duckduckgo_api(new_dict.get('institution'))
        new_dict['description'] = j_data.get('AbstractText', '')
        new_dict['duckduckgo_search'] = duck_url

        data_list.append(clean_university(new_dict))
    return data_list


def clean_university(university):
    """
    Clean university dictionary:
        - if value == '-' -> None
        - if value contain '>' -> update value = value+1
        - strip string, space
    :param university:
    :return:
    """
    for k, v in university.items():
        if isinstance(v, str):
            if v.isdigit():
                university[k] = int(v)
            elif re.match(r'>\s+\d+', v):
                university[k] = int(re.search(r'\d+', v).group())
            elif v.strip() == '-':
                university[k] = None
    return university
