from mongo_to_sql.process.main import main
from mongo_to_sql_tests.constants.postgres import postgres_database_name


def test_main():
    main(postgres_database_name)
