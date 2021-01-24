
import environ
import psycopg2
import psycopg2.extras
from psycopg2 import sql

from mongo_to_sql.databases.utils import list_to_dict, PostgresColumnMapper, PostgresValueCleaner

env = environ.Env(DEBUG=(bool, False))


class PostgresDatabase:
    def __init__(self, dbname=None):
        self.hostname = env("POSTGRES_HOST", default="localhost")
        self.port = env("POSTGRES_PORT", default=27017)
        self.dbname = env("POSTGRES_DBNAME", default="test")
        self.user = env("POSTGRES_USER", default=None)
        self.password = env("POSTGRES_PASSWORD", default=None)
        if dbname:
            self.dbname = dbname

    def insert_multiple_objects_from_mongodb(self, collections_dict):
        for table, collection in collections_dict.items():
            objects_dict = list_to_dict(collection)
            self.insert_multiple_objects_from_dict(objects_dict, table)

    def insert_multiple_objects_from_dict(self, dictionary, table):
        if not self.table_exists_in_postgres(table):
            self.create_table_from_dict(dictionary, table)
        clean_dictionary = PostgresValueCleaner(table, dictionary)
        data = clean_dictionary.format()
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES %s;").format(
            table=sql.Identifier(table),
            fields=sql.SQL(', ').join(
                [*map(sql.Identifier, [field for field in clean_dictionary.clean_dictionary.keys()])]
            )
        )

        with self.create_connection() as conn:
            conn.autocommit = True
            with conn.cursor() as postgres_cursor:
                psycopg2.extras.execute_values(
                    postgres_cursor, query, data, template=None, page_size=100
                )

    def create_connection(self):
        return psycopg2.connect(
            host=self.hostname, port=self.port, dbname=self.dbname, user=self.user, password=self.password
        )

    def table_exists_in_postgres(self, table):
        exists = False
        query = sql.SQL("select exists(select relname from pg_class where relname={table})").format(
            table=sql.Literal(table),
        )
        conn = self.create_connection()
        with conn.cursor() as postgres_cursor:
            postgres_cursor.execute(query)
            exists = postgres_cursor.fetchone()[0]

        return exists

    def create_table_from_dict(self, dictionary, table):
        columns = self.create_postgres_columns(dictionary, table)
        with self.create_connection() as conn:
            conn.autocommit = True
            with conn.cursor() as postgres_cursor:
                postgres_cursor.execute(
                    sql.SQL(f"CREATE TABLE {table} ({columns.as_string(postgres_cursor)})")
                )

    def create_postgres_columns(self, dictionary, table):
        columns = list()
        columns.append(sql.SQL("id serial PRIMARY KEY"))
        for column, values in dictionary.items():
            column_mapper = PostgresColumnMapper(table=table, column=column, values=values, unique=["_id", ])
            postgres_column = column_mapper.create_column_string_postgres()
            columns.append(postgres_column)
        return sql.SQL(", ").join(columns)
