'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_query_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Sunday, April 19th 2020, 3:50:23 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from os.path import isfile
from json import load
from cerberus import Validator
from microbiome.genetics.query_validator import create_query_format_json


QUERY_FORMAT_FILE = "./microbiome/genetics/query_format.json"


def test_valid_validator():
    create_query_format_json()
    if not isfile(QUERY_FORMAT_FILE): assert False, "Cannot find {}".format(QUERY_FORMAT_FILE)
    with open(QUERY_FORMAT_FILE, "r") as file_ptr: query_schema = load(file_ptr)
    Validator(query_schema)
    

# TODO: Add some query tests
# TODO: Add some negative tests