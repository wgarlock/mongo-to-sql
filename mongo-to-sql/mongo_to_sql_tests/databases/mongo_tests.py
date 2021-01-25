import os
import pymongo

from mongo_to_sql.databases.mongo import MongoDatabase
from mongo_to_sql_tests.constants.mongo import (
    default_collection, mongo_database_one, simplest_document, simplest_document_key, simplest_document_value
)
from mongo_to_sql_tests.fixtures.databases.mongo_fixtures import (  # noqa: F401
    create_mongo_database_no_name, create_mongo_database_with_data
)


class TestMongoDatabase:
    def test_mongo_insert(self, create_mongo_database_no_name):  # noqa: F811
        mongo_no_name = MongoDatabase()
        self.run_insert_one_mongo_script(mongo_no_name)
        assert mongo_no_name.get_database()[default_collection].find_one(simplest_document) == simplest_document

    def test_mongo_insert_with_db_name(self, create_mongo_database_with_data):  # noqa: F811
        mongo_name = MongoDatabase(dbname=mongo_database_one)
        self.run_insert_one_mongo_script(mongo_name)
        assert mongo_name.get_database()[default_collection].find_one(simplest_document) == simplest_document

    def test_get_mongodb_database_collection(self, create_mongo_database_with_data):  # noqa: F811
        mongo_name = MongoDatabase(dbname=mongo_database_one)
        assert mongo_name.get_database()[default_collection] == \
            mongo_name.get_mongodb_database_collection(default_collection)

    def test_get_mongodb_collection_names(self, create_mongo_database_with_data):  # noqa: F811
        mongo_name = MongoDatabase(dbname=mongo_database_one)
        assert default_collection in mongo_name.get_mongodb_collection_names()

    def test_get_documents_from_all_collections(self, create_mongo_database_with_data):  # noqa: F811
        mongo_name = MongoDatabase(dbname=mongo_database_one)
        collection_dict = mongo_name.get_documents_from_all_collections()
        assert default_collection in collection_dict.keys()
        assert collection_dict[default_collection][0][simplest_document_key] == simplest_document_value

    def test_collection_with_authentication(self, create_mongo_database_with_data):  # noqa: F811
        mongo_name = MongoDatabase(dbname=mongo_database_one)
        db = mongo_name.get_database()
        db.add_user("never", password="do_this_in_production")
        user = "never"
        pwd = "do_this_in_production"
        self.add_user(db, user, pwd)
        os.environ["MONGO_USER"] = user
        os.environ["MONGO_PASSWORD"] = pwd
        mongo_name_two = MongoDatabase(dbname=mongo_database_one)
        assert mongo_name.get_mongo_string() != mongo_name_two.get_mongo_string()
        os.environ["MONGO_USER"] = ''
        os.environ["MONGO_PASSWORD"] = ''

    # Support methods to improve readability of tests above

    def run_insert_one_mongo_script(self, mongo):
        db = mongo.get_database()
        collection = db[default_collection]
        collection.insert_one(simplest_document)

    def run_find_one_mongo_script(self, mongo):
        db = mongo.get_database()
        collection = db[default_collection]
        doc = collection.find_one(simplest_document)
        return doc

    def add_user(self, db, user, password):
        try:
            db.command("createUser", user, pwd=password, roles=["read"])
        except pymongo.errors.OperationFailure:
            db.command("updateUser", user, pwd=password, roles=["read"])
