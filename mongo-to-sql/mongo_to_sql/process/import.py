import environ
import os

from mongo_to_sql.databases import mongo, postgres


directory = '/Users/wgarlock/Documents/all_collections'
root = environ.Path(__file__) - 4
BASE_DIR = root()
env = environ.Env(DEBUG=(bool, False))
env.read_env(os.path.join(BASE_DIR, '.migrate_config'))
mongo_database = mongo.MongoDatabase()
if directory and os.path.exists(directory):
    mongo_database.post_collections_from_directory(directory=directory)
else:
    #TODO Better Exception here
    raise Exception("You must specify an absolute path to a directory {directory} does not exist")

