'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_query_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Sunday, April 19th 2020, 3:50:23 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

import pytest
from os.path import join, dirname
from json import load
from microbiome.genetics.query_validator import query_validator
from microbiome.genetics.entry_column_meta_validator import entry_column_meta_validator
from logging import getLogger, basicConfig, DEBUG


basicConfig(filename='erasmus.log', level=DEBUG)
queries = load(open(join(dirname(__file__), "test_entry_queries.json"), "r"))
schema = load(open(join(dirname(__file__), "test_entry_format.json"), "r"))
for k, v in schema.items(): v['meta'] = entry_column_meta_validator.normalized(v['meta'])


def test_query_validator_init():
    validator = query_validator(schema, "test")
    validator.create_query_format_json()


@pytest.mark.parametrize("query", queries)
def test_query_validation(query):
    validator = query_validator(schema, "test")
    assert validator.validate(query), str(validator.errors)




