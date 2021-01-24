import pytest
from mongo_to_sql.databases.postgres import PostgresDatabase
from mongo_to_sql_tests.constants.postgres import postgres_database_name
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


@pytest.fixture(scope="module")
def test_postgres_database():
    pg_db = PostgresDatabase(dbname="postgres")
    conn = pg_db.create_connection()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as postgres_cursor:
        sqlCreateDatabase = 'create database {db}'.format(
                db=postgres_database_name
            )
        yield postgres_cursor.execute(sqlCreateDatabase)

    with conn.cursor() as postgres_cursor:
        sqlDisconnect = (
            "SELECT pg_terminate_backend(pid)"
            " FROM pg_stat_activity WHERE datname = '{db}';"
        ).format(db=postgres_database_name)
        postgres_cursor.execute(sqlDisconnect)
        sqlDeleteDatabase = 'drop database {db}'.format(
            db=postgres_database_name
        )
        postgres_cursor.execute(sqlDeleteDatabase)
