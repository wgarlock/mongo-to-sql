import os
import pytest
import subprocess

from mongo_to_sql.databases.mongo import MongoDatabase
from mongo_to_sql_tests.constants.mongo import mongo_database_one  # noqa: F401


@pytest.fixture(scope="class")
def create_mongo_database_no_name():
    db = MongoDatabase()
    yield db.get_database()
    db.drop_database()


@pytest.fixture(scope="session")
def create_mongo_database_with_data():
    db = MongoDatabase(dbname=mongo_database_one)
    path_to_collection = os.path.join('mongo-to-sql', 'mongo_to_sql_tests', 'fixtures', 'testing_mongo', 'zips.bson')
    option = f'--uri="{MongoDatabase(dbname=mongo_database_one).get_mongo_string()}"'
    collection = subprocess.run(["mongorestore", option, path_to_collection])
    print("The exit code was: %d" % collection.returncode)
    yield db.get_database()
    db.drop_database()
