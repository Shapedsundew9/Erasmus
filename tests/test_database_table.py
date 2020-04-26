'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_database_table.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Saturday, April 25th 2020, 6:10:10 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


import pytest
import logging
from os.path import join, dirname
from json import load
from microbiome.genetics.query_validator import query_validator
from microbiome.genetics.config import set_config, get_config
from microbiome.genetics.database_table import database_table
from logging import getLogger


test_config = load(open(join(dirname(__file__), "test_config.json"), "r"))
queries = load(open(join(dirname(__file__), "test_entry_queries.json"), "r"))
results = load(open(join(dirname(__file__), "test_entry_results.json"), "r"))
schema = load(open(join(dirname(__file__), "test_entry_format.json"), "r"))
logging.basicConfig(filename='erasmus.log', level=logging.DEBUG)


@pytest.fixture(scope="module")
def test_table():
    data = load(open(join(dirname(__file__), "test_entry_data.json"), "r"))
    set_config(test_config)
    table = database_table(getLogger(__file__), "test_table", get_config(["data_stores","test_table"]), schema)
    table.store(data)
    return table


@pytest.mark.parametrize("index", list(range(len(queries))))
def test_db_load(index, test_table):
    query = queries[index]
    result = results[index]
    assert test_table.load(query) == result
    

