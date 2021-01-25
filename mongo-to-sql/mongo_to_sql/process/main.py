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
