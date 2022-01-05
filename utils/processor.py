import re
import pandas as pd

from io import StringIO
from utils.environments import create_environments

env = create_environments()


def parse_year_from_file_name(filename):
    return int(re.search(r'\d+', filename).group())


# noinspection PyBroadException
def process_data(file_data):
    data_file = pd.read_csv(StringIO(str(file_data, 'utf-8')), sep='\t')
    data_list = list()
    for _, row in data_file[1:].iterrows():
        new_dict = dict()
        for i in zip(data_file.columns, row):
            new_dict[re.sub(r'\s+', ' ', i[0].strip().lower())] = i[1]
        data_list.append(clean_university(new_dict))
    return data_list


def clean_university(university):
    for k, v in university.items():
        if isinstance(v, str):
            if v.isdigit():
                university[k] = int(v)
            elif re.match(r'>\s+\d+', v):
                university[k] = int(re.search(r'\d+', v).group())
            elif v.strip() == '-':
                university[k] = None
    return university
