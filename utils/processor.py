import pandas as pd
from io import StringIO


def process_data(file_data):
    pd.read_csv(StringIO(file_data), sep='\t')
