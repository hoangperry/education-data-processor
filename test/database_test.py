from utils.database import push_new_document
from utils.environments import create_environments

env = create_environments()


if __name__ == '__main__':
    test_document = {
        'name': 'hoang123123123'
    }
    push_new_document(test_document, collection_name=env.database_university_collection)
