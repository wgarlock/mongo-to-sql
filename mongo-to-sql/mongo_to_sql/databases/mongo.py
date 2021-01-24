
import environ
from pymongo import MongoClient

env = environ.Env(DEBUG=(bool, False))


class MongoDatabase:
    def __init__(self, dbname=None):
        if dbname:
            self.dbname = dbname
        else:
            self.dbname = env("MONGO_DBNAME", default="test")
        self.hostname = env("MONGO_HOST", default="localhost")
        self.port = env("MONGO_PORT", default=27017)
        self.user = env("MONGO_USER", default=None)
        self.password = env("MONGO_PASSWORD", default=None)
        self.client = MongoClient(self.get_mongo_string())

    def get_mongo_string(self):
        if self.user and self.password:
            return f"mongodb://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.dbname}"
        else:
            return f"mongodb://{self.hostname}:{self.port}/{self.dbname}"

    def drop_database(self):
        with self.client as mongo_client:
            print(self.dbname)
            mongo_client.drop_database(self.dbname)
            mongo_client.drop_database(self.dbname)

    def get_database(self):
        with self.client as mongo_client:
            return getattr(mongo_client, self.dbname)

    def get_mongodb_database_collection(self, collection):
        database = self.get_database()
        return getattr(database, collection)

    def get_mongodb_collection_names(self):
        database = self.get_database()
        return database.list_list_collection_names()

    def get_documents_from_collection(self, collection):
        return list(self.get_mongodb_database_collection(collection).find())[:10]

    def get_documents_from_all_collections(self):
        collections = dict()
        list_collection_names = self.get_mongodb_collection_names()
        [collections.update({name: self.get_documents_from_collection(name)}) for name in list_collection_names]
        return collections
