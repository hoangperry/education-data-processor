from pymongo import MongoClient
from utils.environments import create_environments

env = create_environments()


def create_mongo_url_connection(username=None, password=None, host=None, port=None, database_name=None):
    username = env.database_username if username is None else username
    password = env.database_password if password is None else password
    host = env.database_host if host is None else host
    port = env.database_port if port is None else port
    database_name = env.database_name if database_name is None else database_name

    return f'mongodb://{username}:{password}@{host}:{port}/{database_name}'


def create_connection(connection_url=None):
    connection_url = create_mongo_url_connection() if connection_url is None else connection_url
    return MongoClient(connection_url)


def push_new_document(document, collection_name, client_connection=None):
    if client_connection is None:
        create_connection()
        connection_already_existed = False
    else:
        connection_already_existed = True

    client_connection[collection_name].insert(document)

    if not connection_already_existed:
        client_connection.close()
