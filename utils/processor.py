import pandas as pd

from io import StringIO
from utils.database import push_new_document
from utils.environments import create_environments

env = create_environments()


def process_data(file_data):
    data_file = pd.read_csv(StringIO(file_data), sep='\t')
    data_list = list()
    for _, row in data_file[1:].iterrows():
        new_dict = dict()
        for i in zip(data_file.columns, row):
            new_dict[i[0]] = i[1]
        push_new_document(new_dict, env.database_university_collection)
        data_list.append(new_dict)
    push_new_document(data_list, env.database_year_collection)
