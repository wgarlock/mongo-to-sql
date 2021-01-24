import pytest
from mongo_to_sql.databases.mongo import MongoDatabase
from mongo_to_sql_tests.constants.mongo import mongo_database_one, mongo_database_two


@pytest.fixture(scope="class")
def create_mongo_database_no_name():
    db = MongoDatabase()
    yield db.get_database()
    db.drop_database()


@pytest.fixture(scope="class")
def create_mongo_database_one():
    db = MongoDatabase(dbname=mongo_database_one)
    yield db.get_database()
    db.drop_database()


@pytest.fixture(scope="class")
def create_mongo_database_two():
    db = MongoDatabase(dbname=mongo_database_two)
    yield db.get_database()
    db.drop_database()
