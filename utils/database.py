import re
import urllib.parse

from pymongo import MongoClient
from utils.environments import create_environments

env = create_environments()


def create_mongo_url_connection(username=None, password=None, host=None, port=None) -> str:
    """
    :param username:
    :param password:
    :param host:
    :param port:
    :return: mongodb connection string
    """
    # Using default environment variable
    username = urllib.parse.quote(env.database_username if username is None else username)
    password = urllib.parse.quote(env.database_password if password is None else password)
    host = urllib.parse.quote(env.database_host if host is None else host)
    port = urllib.parse.quote(env.database_port if port is None else port)
    return f'mongodb://{username}:{password}@{host}:{port}/'


def create_connection(connection_url=None) -> MongoClient:
    """
    :param connection_url:
    :return: MongoDb client
    """
    connection_url = create_mongo_url_connection() if connection_url is None else connection_url
    return MongoClient(connection_url)


def get_uni_by_institution(institution, database_name=None, client_connection=None) -> dict:
    """
    Query university by institution name (ignore case)
    :param institution:
    :param database_name:
    :param client_connection:
    :return: dictionary of university
    """
    # Create a new client connection if the caller doesn't pass in any
    database_name = env.database_name if database_name is None else database_name
    if client_connection is None:
        client_connection = create_connection()
        connection_already_existed = False
    else:
        connection_already_existed = True
    uni = client_connection[database_name][env.database_university_collection].find_one(
        {'institution': re.compile(institution, re.IGNORECASE)}
    )
    if not connection_already_existed:
        client_connection.close()
    if uni is None:
        return dict()
    try:
        del uni['_id']
    except:
        pass
    return uni


def push_new_document(document, collection_name, database_name=None, client_connection=None):
    """
    Push new document to mongodb by collection name or update document if institution is existed (Ignore case)
    :param document:
    :param collection_name:
    :param database_name:
    :param client_connection:
    :return:
    """
    database_name = env.database_name if database_name is None else database_name
    # Create a new client connection if the caller doesn't pass in any
    if client_connection is None:
        client_connection = create_connection()
        connection_already_existed = False
    else:
        connection_already_existed = True

    if collection_name == env.database_university_collection:
        client_connection[database_name][collection_name].find_one_and_update(
            {'institution': re.compile(document.get('institution', None), re.IGNORECASE)},
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
