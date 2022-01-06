import os


class ConfigDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def create_environments():
    """
    Create argument based on file name and environment variables
    """

    configs = dict()
    # Database config
    configs['database_username'] = str(os.environ.get('DATABASE_USERNAME', 'hoangntruong'))
    configs['database_password'] = str(os.environ.get('DATABASE_PASSWORD', 'NYTPnHoang'))
    configs['database_host'] = str(os.environ.get('DATABASE_HOST', 'ai.hoang.tech'))
    configs['database_port'] = str(os.environ.get('DATABASE_PORT', '27018'))
    configs['database_name'] = str(os.environ.get('DATABASE_NAME', 'edu_db'))

    configs['database_year_collection'] = str(os.environ.get('DATABASE_YEAR_COL', 'year_c'))
    configs['database_university_collection'] = str(os.environ.get('DATABASE_UNI_COL', 'uni_c'))
    return ConfigDict(configs)
