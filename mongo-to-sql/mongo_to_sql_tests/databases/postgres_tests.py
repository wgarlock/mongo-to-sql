import os
from mongo_to_sql.databases.exceptions import DataDictionaryMalformed, InconsistentMongoDBData
from mongo_to_sql.databases.postgres import PostgresDatabase
from mongo_to_sql.databases.utils import (
    create_clean_field_string, list_to_dict, PostgresColumnMapper, PostgresValueCleaner
)
from mongo_to_sql_tests.constants.mongo import collection_response, collection_response_zips
from mongo_to_sql_tests.constants.postgres import (
    clean_table_name, column_mapper_key_bool, column_mapper_key_city, column_mapper_key_dict, column_mapper_key_float,
    column_mapper_key_id, column_mapper_key_large_text, column_mapper_key_loc, column_mapper_key_pop,
    column_mapper_key_state, column_mapper_key_tuple, column_mapper_values, column_mapper_values_dict,
    inconsistent_column_mapper_values, postgres_database_name, string_format_constants, unique_list_with_id
)
from mongo_to_sql_tests.fixtures.databases.postgres_fixtures import test_postgres_database  # noqa: F401
from psycopg2 import sql


class TestPostgresDatabase:
    pg_db = PostgresDatabase(dbname=postgres_database_name)
    dict_obj = list_to_dict(collection_response_zips)

    # Some of these modules implictly rely on envirnonment variables that are
    # defined in create_env_vars.

    # TODO create assertions

    def test_init_create_connnection_with_env_vars(self, test_postgres_database):  # noqa: F811
        os.environ["POSTGRES_DBNAME"] = postgres_database_name
        conn = self.pg_db.create_connection()  # noqa: F841

    # TODO create assertions
    def test_init_create_connnection_with_existing_db_name(self, test_postgres_database):  # noqa: F811
        pg_db = PostgresDatabase(dbname=postgres_database_name)
        conn = pg_db.create_connection()  # noqa: F841

    def test_create_postgres_columns(self):
        sql_statement = self.pg_db.create_postgres_columns(self.dict_obj, clean_table_name)
        assert isinstance(sql_statement, sql.Composed)
        # TODO more asserts to establish validity of response

    def test_create_table_from_dict(self, test_postgres_database):  # noqa: F811
        self.pg_db.create_table_from_dict(self.dict_obj, clean_table_name)
        assert self.pg_db.table_exists_in_postgres(clean_table_name)

    def test_table_exists_in_postgres_does_not_exist(self, test_postgres_database):  # noqa: F811
        assert not self.pg_db.table_exists_in_postgres("does_not_exist")

    def test_insert_multiple_objects_from_dict(self, test_postgres_database):  # noqa: F811
        self.pg_db.insert_multiple_objects_from_dict(self.dict_obj, clean_table_name)

    def test_insert_multiple_objects_from_mongodb(self, test_postgres_database):  # noqa: F811
        self.pg_db.insert_multiple_objects_from_mongodb(collection_response)


class TestPostgresColumnMapper:
    pg_db = PostgresDatabase(dbname=postgres_database_name)
    dict_obj = list_to_dict(column_mapper_values)
    inconsistent_dict_obj = list_to_dict(inconsistent_column_mapper_values)

    def test_init_postgres_columns(self, test_postgres_database):  # noqa: F811
        mapper = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_city,
            values=self.dict_obj[column_mapper_key_city],
            unique=unique_list_with_id
        )
        column_mapper_type_index_zero = type(self.dict_obj[column_mapper_key_city][0])

        assert mapper.table == clean_table_name
        assert mapper.column == column_mapper_key_city
        assert mapper.values == self.dict_obj[column_mapper_key_city]
        assert mapper.values_type == column_mapper_type_index_zero
        assert mapper.primitive_name == column_mapper_type_index_zero.__name__
        assert mapper.unique == unique_list_with_id
        assert mapper.clean_column is None
        assert mapper.data_type is None
        assert mapper.constraints is None

    def test_handle_string(self):
        desired_output = "text"
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_city,
            values=self.dict_obj[column_mapper_key_city],
            unique=unique_list_with_id
        )
        assert mapper_one.handle_string() == desired_output
        assert mapper_one.select_data_type() == desired_output

        desired_output = "varchar(2)"
        mapper_two = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_state,
            values=self.dict_obj[column_mapper_key_state],
            unique=unique_list_with_id
        )
        assert mapper_two.handle_string() == desired_output
        assert mapper_two.select_data_type() == desired_output

        desired_output = "varchar(5)"
        mapper_three = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_id,
            values=self.dict_obj[column_mapper_key_id],
            unique=unique_list_with_id
        )
        assert mapper_three.handle_string() == desired_output
        assert mapper_three.select_data_type() == desired_output

        desired_output = "text"
        mapper_four = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_large_text,
            values=self.dict_obj[column_mapper_key_large_text],
            unique=unique_list_with_id)
        assert mapper_four.handle_string() == desired_output
        assert mapper_four.select_data_type() == desired_output

    def test_handle_integer(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_pop,
            values=self.dict_obj[column_mapper_key_pop],
            unique=unique_list_with_id
        )
        desired_output = "integer"
        assert mapper_one.handle_integer() == desired_output
        assert mapper_one.select_data_type() == desired_output

    def test_handle_float(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_float,
            values=self.dict_obj[column_mapper_key_float],
            unique=unique_list_with_id
        )
        desired_output = "decimal"
        assert mapper_one.handle_float() == desired_output
        assert mapper_one.select_data_type() == desired_output

    def test_handle_boolean(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_bool,
            values=self.dict_obj[column_mapper_key_bool],
            unique=unique_list_with_id
        )
        desired_output = "boolean"
        assert mapper_one.handle_boolean() == desired_output
        assert mapper_one.select_data_type() == desired_output

    def test_handle_list(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_loc,
            values=self.dict_obj[column_mapper_key_loc],
            unique=unique_list_with_id
        )
        desired_output = "jsonb"
        assert mapper_one.handle_list() == desired_output
        assert mapper_one.select_data_type() == desired_output

    def test_handle_dict(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_dict,
            values=self.dict_obj[column_mapper_key_dict],
            unique=unique_list_with_id
        )
        desired_output = "jsonb"
        assert mapper_one.handle_dict() == desired_output
        assert mapper_one.select_data_type() == desired_output

    def test_handle_tuple(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_tuple,
            values=self.dict_obj[column_mapper_key_tuple],
            unique=unique_list_with_id
        )
        desired_output = "jsonb"
        assert mapper_one.handle_tuple() == desired_output
        assert mapper_one.select_data_type() == desired_output

    def test_has_consistent_data(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_city,
            values=self.dict_obj[column_mapper_key_city],
            unique=unique_list_with_id
        )
        assert mapper_one.has_consistent_data()

    def test_has_consistent_data_error(self):
        boolean_value = False
        try:
            mapper_one = PostgresColumnMapper(
                table=clean_table_name,
                column=column_mapper_key_id,
                values=self.inconsistent_dict_obj[column_mapper_key_id], unique=unique_list_with_id)
            mapper_one.has_consistent_data()
        except InconsistentMongoDBData:
            boolean_value = True

        assert boolean_value

    def test_create_constraints(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_city,
            values=self.dict_obj[column_mapper_key_city], unique=unique_list_with_id)
        mapper_one.create_constraints()
        assert mapper_one.constraints == "NOT NULL"

    def test_create_constraints_null_entries(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_pop,
            values=self.inconsistent_dict_obj[column_mapper_key_pop],
            unique=unique_list_with_id
        )
        mapper_one.create_constraints()
        assert mapper_one.constraints == ""

    def test_create_constraints_unique_entries(self):
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_id,
            values=self.inconsistent_dict_obj[column_mapper_key_id],
            unique=unique_list_with_id
        )
        mapper_one.create_constraints()
        assert mapper_one.constraints == "NOT NULL UNIQUE"

    def test_create_column_string_postgres(self):
        conn = self.pg_db.create_connection()
        mapper_one = PostgresColumnMapper(
            table=clean_table_name,
            column=column_mapper_key_id,
            values=self.dict_obj[column_mapper_key_id],
            unique=unique_list_with_id
        )
        sql_column_string = mapper_one.create_column_string_postgres()
        with conn.cursor() as postgres_cursor:
            column_string = sql_column_string.as_string(postgres_cursor)
            assert "UNIQUE" in column_string
            assert "NOT NULL" in column_string
            assert "varchar(5)" in column_string
            assert column_mapper_key_id in column_string

    def test_create_column_string_postgres_data_error(self):
        boolean_value = False
        try:
            mapper_one = PostgresColumnMapper(
                table=clean_table_name,
                column=column_mapper_key_id,
                values=self.inconsistent_dict_obj[column_mapper_key_id],
                unique=unique_list_with_id
            )
            mapper_one.create_column_string_postgres()
        except InconsistentMongoDBData:
            boolean_value = True

        assert boolean_value


class TestPostgresValueCleaner:
    cleaned_values = PostgresValueCleaner(table=clean_table_name, dictionary=column_mapper_values_dict)

    def test_init_postgres_value_cleaner(self):
        assert self.cleaned_values.table == clean_table_name
        assert self.cleaned_values.dictionary == column_mapper_values_dict
        assert self.cleaned_values.clean_dictionary == dict()
        assert self.cleaned_values.objects == list()

    def test_append_to_objects_tuple(self):
        self.cleaned_values.append_to_objects_list(0, "test_one")
        self.cleaned_values.append_to_objects_list(1, "test_two")
        assert len(self.cleaned_values.objects) == 2
        assert self.cleaned_values.objects[0] == ("test_one", )
        self.cleaned_values = list()

    def test_handle_string(self):
        value = self.cleaned_values.handle_string(
            column_mapper_key_city,
            column_mapper_values_dict[column_mapper_key_city]
        )
        assert isinstance(value, tuple)
        assert isinstance(value[0], str)
        assert self.cleaned_values.clean_values(
            column_mapper_key_city,
            column_mapper_values_dict[column_mapper_key_city]
        ) == value

    def test_handle_integer(self):
        value = self.cleaned_values.handle_integer(
            column_mapper_key_pop,
            column_mapper_values_dict[column_mapper_key_pop])
        assert isinstance(value, tuple)
        assert isinstance(value[0], int)
        assert self.cleaned_values.clean_values(
            column_mapper_key_pop,
            column_mapper_values_dict[column_mapper_key_pop]
        ) == value

    def test_handle_float(self):
        value = self.cleaned_values.handle_float(
            column_mapper_key_float,
            column_mapper_values_dict[column_mapper_key_float])
        assert isinstance(value, tuple)
        assert isinstance(value[0], float)
        assert self.cleaned_values.clean_values(
            column_mapper_key_float,
            column_mapper_values_dict[column_mapper_key_float]
        ) == value

    def test_handle_boolean(self):
        value = self.cleaned_values.handle_boolean(
            column_mapper_key_bool,
            column_mapper_values_dict[column_mapper_key_bool])
        assert isinstance(value, tuple)
        assert isinstance(value[0], bool)
        assert self.cleaned_values.clean_values(
            column_mapper_key_bool,
            column_mapper_values_dict[column_mapper_key_bool]
        ) == value

    def test_handle_list(self):
        value = self.cleaned_values.handle_list(
            column_mapper_key_loc, column_mapper_values_dict[column_mapper_key_loc])
        assert isinstance(value, tuple)
        assert isinstance(value[0], str)
        assert self.cleaned_values.clean_values(
            column_mapper_key_loc, column_mapper_values_dict[column_mapper_key_loc]
        ) == value

    def test_handle_dict(self):
        value = self.cleaned_values.handle_dict(
            column_mapper_key_dict,
            column_mapper_values_dict[column_mapper_key_dict])
        assert isinstance(value, tuple)
        assert isinstance(value[0], dict)
        assert self.cleaned_values.clean_values(
            column_mapper_key_dict,
            column_mapper_values_dict[column_mapper_key_dict]
        ) == value

    def test_handle_tuple(self):
        value = self.cleaned_values.handle_tuple(
            column_mapper_key_tuple,
            column_mapper_values_dict[column_mapper_key_tuple]
        )
        assert isinstance(value, tuple)
        assert isinstance(value[0], tuple)
        assert self.cleaned_values.clean_values(
            column_mapper_key_tuple,
            column_mapper_values_dict[column_mapper_key_tuple]
        ) == value

    def test_create_object_tuples(self):
        self.cleaned_values.objects = list()
        self.cleaned_values.create_object_tuples(column_mapper_values_dict[column_mapper_key_bool])
        self.cleaned_values.create_object_tuples(column_mapper_values_dict[column_mapper_key_city])

        assert isinstance(self.cleaned_values.objects, list)
        assert isinstance(self.cleaned_values.objects[0], tuple)
        assert isinstance(self.cleaned_values.objects[0][0], bool)
        assert isinstance(self.cleaned_values.objects[0][1], str)

    def test_create_clean_dictionary_return_key(self):
        value = self.cleaned_values.create_clean_dictionary_return_values(
            column_mapper_key_city,
            column_mapper_values_dict[column_mapper_key_city]
        )
        assert isinstance(value, tuple)
        assertion_value = False
        try:
            self.cleaned_values.create_clean_dictionary_return_values(column_mapper_key_city, "test")
        except DataDictionaryMalformed:
            assertion_value = True

        assert assertion_value

    def test_format(self):
        tuples = self.cleaned_values.objects = list()
        tuples = self.cleaned_values.format()
        assert isinstance(tuples, tuple)
        assert isinstance(tuples[0], tuple)
        assert len(tuples[0]) == len(column_mapper_values_dict.keys())


def test_create_clean_field_string():
    clean_strings = set()
    for column in string_format_constants:
        clean_strings.add(create_clean_field_string(clean_table_name, column))
    assert len(clean_strings) == 1


def test_list_to_dict():
    dict_obj = list_to_dict(collection_response_zips)
    assert dict_obj.keys() == collection_response_zips[0].keys()
    assert all(isinstance(value, (list, tuple)) for value in dict_obj.values())
