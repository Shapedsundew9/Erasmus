'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/query_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, April 19th 2020, 2:42:22 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from os.path import dirname, join
from json import load, dump
from cerberus import Validator


def __query_params(entry_schema):
    param_schema = {
        'type': [entry_schema['type'], 'list'],
        'schema': {
            'type': entry_schema['type'],
        }
    }
    if entry_schema['type'] == "integer" or entry_schema['type'] == "float" or entry_schema['meta']['database']['type'] == "TIMESTAMP":
        param_schema['schema']['type'] = [param_schema['schema']['type'], "dict"]
        param_schema['schema']['schema'] = {
            "min": {
                'type': entry_schema['type'],
                'required': True
            },
            "max": {
                'type': entry_schema['type'],
                'required': True

            }
        }
    return param_schema


def __create_query_schema():
    query_schema = {k: __query_params(v) for k, v in filter(lambda kv: not kv[1]['meta']['compressed'], load(open(join(dirname(__file__), "entry_format.json"), "r")).items())}
    query_schema['limit']: {
        'type': 'integer',
        'minimum': 1
    }
    query_schema['random']: {
        'type': 'boolean',
        'default': False
    }
    return query_schema


# The query validation schema is derived from the entry validation schema.
QUERY_VALIDATION_SCHEMA = __create_query_schema()
__query_validator = Validator(QUERY_VALIDATION_SCHEMA)


# This function is used in generating the package documentation
def create_query_format_json():
    with open(join(dirname(__file__), "query_format.json"), "w") as file_ptr:
        dump(QUERY_VALIDATION_SCHEMA, file_ptr, indent=4, sort_keys=True)


# Cerberus does not support validation of a top level list
# https://github.com/pyeve/cerberus/issues/220
def query_validator(query):
    if isinstance(query, list):
        for q in query:
            if not __query_validator(q): return False, __query_validator.errors 
        return True, __query_validator.errors
    return __query_validator(query), __query_validator.errors
