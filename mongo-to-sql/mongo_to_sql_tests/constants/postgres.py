from lorem_text import lorem

postgres_database_name = "postgres_test"
postgres_database_name_no_exist = "postgres_test_i_dont_exist"

clean_table_name = "test_table"

column_mapper_key_id = "_id"
column_mapper_key_var_length_string = "city"
column_mapper_key_int = "pop"
column_mapper_key_fixed_len_string = "state"
column_mapper_key_list = "loc"
column_mapper_key_large_text = "large_text"
column_mapper_key_bool = "is_big"
column_mapper_key_float = "area",
column_mapper_key_tuple = "leaders"
column_mapper_key_dict = "city_hall"

column_mapper_values = [
    {
        column_mapper_key_id: "01002",
        column_mapper_key_var_length_string:  "CUSHMAN",
        column_mapper_key_int: 36963,
        column_mapper_key_fixed_len_string: "MA",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: True,
        column_mapper_key_float: 1352374687.06598,
        column_mapper_key_tuple: ("wefwef", "wefwef", "wefwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
    {
        column_mapper_key_id: "01003",
        column_mapper_key_var_length_string:  "CUSHMAN",
        column_mapper_key_int: 36934,
        column_mapper_key_fixed_len_string: "OH",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: False,
        column_mapper_key_float: 135747856786687.55506598,
        column_mapper_key_tuple: ("wefwwefef", "wefweweff", "wefwef", "kjqwdihqwd"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
    {
        column_mapper_key_id: "01004",
        column_mapper_key_var_length_string:  "SHMAN",
        column_mapper_key_int: 36965,
        column_mapper_key_fixed_len_string: "FL",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: True,
        column_mapper_key_float: 13785687.06555598,
        column_mapper_key_tuple: ("wefuiluilwef", "weweffwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
    {
        column_mapper_key_id: "01005",
        column_mapper_key_var_length_string: "MAN",
        column_mapper_key_int: 36963,
        column_mapper_key_fixed_len_string: "GA",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: True,
        column_mapper_key_float: 13574756.98,
        column_mapper_key_tuple: ("wefuiluilwef", "wefwuiluilf", "weuiluilfwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
    {
        column_mapper_key_id: "01006",
        column_mapper_key_var_length_string: "CUSH",
        column_mapper_key_int: 36763,
        column_mapper_key_fixed_len_string: "MA",
        column_mapper_key_list: [
            -74.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: False,
        column_mapper_key_float: 654687.06598,
        column_mapper_key_tuple: ("wwwhhrtwef", "wefwghgergeref", "wefgggjjtyjwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
]

inconsistent_column_mapper_values = [
    {
        column_mapper_key_id:  1002,
        column_mapper_key_var_length_string:   "CUSHMAN",
        column_mapper_key_int:  36963,
        column_mapper_key_fixed_len_string: "MA",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: True,
        column_mapper_key_float: 1352374687.06598,
        column_mapper_key_tuple: ("wefwef", "wefwef", "wefwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }


    },
    {
        column_mapper_key_id:  "01003",
        column_mapper_key_var_length_string:   "CUSHMAN",
        column_mapper_key_int:  36934,
        column_mapper_key_fixed_len_string: "OH",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: False,
        column_mapper_key_float: 135747856786687.55506598,
        column_mapper_key_tuple: ("wefwwefef", "wefweweff", "wefwef", "kjqwdihqwd"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
    {
        column_mapper_key_id:  1004,
        column_mapper_key_var_length_string:   "SHMAN",
        column_mapper_key_fixed_len_string: "FL",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: True,
        column_mapper_key_float: 13785687.06555598,
        column_mapper_key_tuple: ("wefuiluilwef", "weweffwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
    {
        column_mapper_key_id:  "01005",
        column_mapper_key_var_length_string:   "MAN",
        column_mapper_key_int:  36963,
        column_mapper_key_fixed_len_string: "GA",
        column_mapper_key_list: [
            -72.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: "True",
        column_mapper_key_float: 13574756.98,
        column_mapper_key_tuple: ("wefuiluilwef", "wefwuiluilf", "weuiluilfwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
    {
        column_mapper_key_id:  "01006",
        column_mapper_key_var_length_string:   "CUSH",
        column_mapper_key_int:  36763,
        column_mapper_key_fixed_len_string: "MA",
        column_mapper_key_list: [
            -74.51565, 42.377017
        ],
        column_mapper_key_large_text: lorem.words(255),
        column_mapper_key_bool: False,
        column_mapper_key_float: 654687.06598,
        column_mapper_key_tuple: ("wwwhhrtwef", "wefwghgergeref", "wefgggjjtyjwef"),
        column_mapper_key_dict: {
            "name": "home",
            "stories": 3
        }
    },
]

unique_list_with_id = ["_id"]

column_mapper_values_dict = {
    column_mapper_key_id:  ["01002", "01003", "01004", "01005", "01006"],
    column_mapper_key_var_length_string:   ["CUSHMAN", "CUSHMAN", "SHMAN", "MAN", "CUSH"],
    column_mapper_key_int:  [36963, 36934, 36965, 36963, 36763],
    column_mapper_key_fixed_len_string: ["MA", "OH", "FL", "GS", "MA"],
    column_mapper_key_list: [
        [
            -72.51565, 42.377017
        ],
        [
            -72.51565, 42.377017
        ],
        [
            -72.51565, 42.377017
        ],
        [
            -72.51565, 42.377017
        ],
        [
            -72.51565, 42.377017
        ],
    ],
    column_mapper_key_large_text: [
        lorem.words(255),
        lorem.words(255),
        lorem.words(255),
        lorem.words(255),
        lorem.words(255)
    ],
    column_mapper_key_bool: [True, False, True, True, False],
    column_mapper_key_float: [1352374687.06598, 135747856786687.55506598, 13785687.06555598, 13574756.98, 654687.06598],
    column_mapper_key_tuple: [
        ("wefwef", "wefwef", "wefwef"),
        ("wefwwefef", "wefweweff", "wefwef", "kjqwdihqwd"),
        ("wefuiluilwef", "weweffwef"),
        ("wefuiluilwef", "wefwuiluilf", "weuiluilfwef"),
        ("wwwhhrtwef", "wefwghgergeref", "wefgggjjtyjwef"),
    ],
    column_mapper_key_dict: [
        {
            "name": "home",
            "stories": 3
        },
        {
            "name": "home",
            "stories": 3
        },
        {
            "name": "home",
            "stories": 3
        },
        {
            "name": "home",
            "stories": 3
        },
        {
            "name": "home",
            "stories": 3
        },
    ]
}

string_format_constants = [
    "_test_id",
    "test_id_",
    "test__id"
]
