import json
from psycopg2 import sql
from statistics import mean, stdev

from mongo_to_sql.databases.exceptions import DataDictionaryMalformed, InconsistentMongoDBData


class PostgresColumnMapper:
    def __init__(self, table, column, values, unique=[]):
        self.table = table
        self.column = column
        self.values = values
        self.values_type = type(self.values[0])
        self.primitive_name = self.values_type.__name__
        self.primitive_mapper = {
            "str": self.handle_string,
            "int": self.handle_integer,
            "float": self.handle_float,
            "bool": self.handle_boolean,
            "list": self.handle_list,
            "dict": self.handle_dict,
            "tuple": self.handle_tuple
        }
        self.unique = unique
        self.clean_column = None
        self.data_type = None
        self.constraints = None

    def create_column_string_postgres(self):
        if self.has_consistent_data():
            self.clean_column = create_clean_field_string(self.table, self.column)
            self.create_constraints()
            self.data_type = self.select_data_type()
            return sql.SQL(f"{self.clean_column} {self.data_type} {self.constraints}")
        else:
            raise InconsistentMongoDBData("One or more indicies in {column} do not match the initial index")

    def has_consistent_data(self):
        if all(isinstance(value, type(self.values[0])) or value is None for value in self.values[1:]):
            return True
        else:
            raise InconsistentMongoDBData("One or more indicies in {column} do not match the initial index")

    def create_constraints(self):
        if not any(value is None for value in self.values[1:]):
            self.constraints = "NOT NULL"
        else:
            self.constraints = ''

        if self.column in self.unique:
            self.constraints += " UNIQUE"

    def select_data_type(self):
        primitive_handler = self.get_primitive_mapper()
        handler = primitive_handler.get(self.primitive_name)
        return handler()

    def get_primitive_mapper(self):
        return self.primitive_mapper

    def handle_string(self):
        lengths = [len(value) for value in self.values]
        length_max = max(lengths)
        lengths_mean = mean(lengths)
        lengths_stdev = stdev(lengths)
        if length_max > 255:
            return "text"
        elif lengths_stdev == 0:
            return f"varchar({lengths_mean})"
        else:
            return "text"

    def handle_integer(self):
        return "integer"

    def handle_float(self):
        return "decimal"

    def handle_boolean(self):
        return "boolean"

    def handle_list(self):
        return "jsonb"

    def handle_dict(self):
        return "jsonb"

    def handle_tuple(self):
        self.values = list(self.values)
        return "jsonb"


class PostgresValueCleaner:
    def __init__(self, table, dictionary):
        self.table = table
        self.dictionary = dictionary
        self.clean_dictionary = dict()
        self.primitive_handlers = {
            "str": self.handle_string,
            "int": self.handle_integer,
            "float": self.handle_float,
            "bool": self.handle_boolean,
            "list": self.handle_list,
            "dict": self.handle_dict,
            "tuple": self.handle_tuple
        }
        self.objects = list()

    def format(self):
        for key, values in self.dictionary.items():
            cleaned_values = self.create_clean_dictionary_return_values(key, values)
            self.create_object_tuples(cleaned_values)
        return tuple(self.objects)

    def create_clean_dictionary_return_values(self, key, values):
        if isinstance(values, (list, tuple)):
            values = self.clean_values(key, values)
            key = create_clean_field_string(self.table, key)
            self.clean_dictionary[key] = values
            return values
        else:
            raise DataDictionaryMalformed(f"{values} malformed")

    def create_object_tuples(self, values):
        [self.append_to_objects_list(idx, value) for idx, value in enumerate(values)]

    def clean_values(self, key, values):
        value_type = type(values[0]).__name__
        handler = self.get_primitive_handlers().get(value_type)
        return handler(key, values)

    def get_primitive_handlers(self):
        return self.primitive_handlers

    def handle_string(self, key, values):
        return tuple(values)

    def handle_integer(self, key, values):
        return tuple(values)

    def handle_float(self, key, values):
        return tuple(values)

    def handle_boolean(self, key, values):
        return tuple(values)

    def handle_list(self, key, values):
        return tuple([json.dumps({key: value}) for value in values])

    def handle_dict(self, key, values):
        return tuple(values)

    def handle_tuple(self, key, values):
        return tuple(values)

    def append_to_objects_list(self, idx, value):
        value_in_tuple = (value,)
        try:
            self.objects[idx] += value_in_tuple
        except IndexError:
            self.objects.append(value_in_tuple)


def create_clean_field_string(table, column):
    iniital_append = "{table}_{column}"
    if "__" in column:
        column = column.replace("__", "_")
    if column[-1] == "_":
        column = column[:-1]
    if column[0] == "_":
        column = column[1:]
    return iniital_append.format(table=table, column=column)


def list_to_dict(list_obj):
    return {
        k: [d.get(k) for d in list_obj]
        for k in set().union(*list_obj)
    }
