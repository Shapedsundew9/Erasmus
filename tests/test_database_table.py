'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_database_table.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Saturday, April 25th 2020, 6:10:10 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


import pytest
from os.path import join, dirname
from json import load
from microbiome.genetics.query_validator import query_validator
from microbiome.genetics.entry_column_meta_validator import entry_column_meta_validator
from microbiome.genetics.config import set_config, get_config
from microbiome.genetics.database_table import database_table
from logging import getLogger


queries = load(open(join(dirname(__file__), "test_entry_queries.json"), "r"))


def test_database_table_create():
    test_config = load(open(join(dirname(__file__), "test_config.json"), "r"))
    data = load(open(join(dirname(__file__), "test_entry_data.json"), "r"))
    schema = load(open(join(dirname(__file__), "test_entry_format.json"), "r"))
    for v in schema.values(): v['meta'] = entry_column_meta_validator.normalized(v['meta'])
    set_config(test_config)
    test_table = database_table(getLogger(__file__), "test_table", get_config("test_table"), schema)
    test_table.store(data)
    

