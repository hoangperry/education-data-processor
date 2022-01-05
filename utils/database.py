from pymongo import MongoClient
from utils.environments import create_environments

env = create_environments()


def create_mongo_url_connection(username=None, password=None, host=None, port=None):
    username = env.database_username if username is None else username
    password = env.database_password if password is None else password
    host = env.database_host if host is None else host
    port = env.database_port if port is None else port

    return f'mongodb://{username}:{password}@{host}:{port}/'


def create_connection(connection_url=None):
    connection_url = create_mongo_url_connection() if connection_url is None else connection_url
    return MongoClient(connection_url)


def push_new_document(document, collection_name, database_name=None, client_connection=None):
    database_name = env.database_name if database_name is None else database_name
    if client_connection is None:
        client_connection = create_connection()
        connection_already_existed = False
    else:
        connection_already_existed = True
    if collection_name == env.database_university_collection:
        client_connection[database_name][collection_name].find_one_and_update(
            {'institution': document.get('institution', None)},
            {"$set": document},
            upsert=True,
        )
    elif collection_name == env.database_year_collection:
        client_connection[database_name][collection_name].find_one_and_update(
            {'year': document.get('year', None)},
            {"$set": document},
            upsert=True,
        )
    else:
        pass

    if not connection_already_existed:
        client_connection.close()
