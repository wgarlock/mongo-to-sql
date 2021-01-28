import environ
import os

from mongo_to_sql.databases import mongo, postgres


def main(dbname=None):
    root = environ.Path(__file__) - 4
    BASE_DIR = root()
    env = environ.Env(DEBUG=(bool, False))
    env.read_env(os.path.join(BASE_DIR, '.migrate_config'))
    mongo_database = mongo.MongoDatabase()
    postgres_database = postgres.PostgresDatabase(dbname=dbname)
    results = mongo_database.get_documents_from_all_collections()
    postgres_database.insert_multiple_objects_from_mongodb(results)

def import_json_from_directory(dbname=None, directory=None):
    mongo_database = mongo.MongoDatabase()
    if directory and os.path.exists(directory):
        mongo_database.post_collections_from_directory(directory=directory)
    else:
        #TODO Better Exception here
        raise Exception("You must specify an absolute path to a directory {directory} does not exist")

