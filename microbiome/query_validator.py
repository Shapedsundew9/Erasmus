'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/query_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, April 19th 2020, 2:42:22 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from os.path import dirname, join
from json import load, dump, loads
from cerberus import Validator
from .entry_column_meta_validator import entry_column_meta_validator


class query_validator():


    _QUERY_BASE_SCHEMA = {
        'order by': {
            'type': 'string'
        },
        'limit': {
            'type': 'integer',
            'min': 1
        },
        'random': {
            'type': 'boolean',
            'default': False
        }
    }


    def __init__(self, table_schema, table_name=""):
        self.table_name = table_name
        queriable_fields = filter(lambda kv: not 'compressed' in kv[1]['meta'] or not kv[1]['meta']['compressed'], table_schema.items())
        validation_schema = {k: self._query_params(v) for k, v in queriable_fields}
        validation_schema.update(query_validator._QUERY_BASE_SCHEMA)
        validation_schema['order by']['allowed'] = [k for k, v in filter(lambda kv: kv[1]['meta']['database']['type'] != 'BYTEA', table_schema.items())]
        self._validator = Validator(validation_schema)
        self.errors = None


    # TODO: Why does this not draw on the entry_schema for rules on validation of the search terms
    def _query_params(self, entry_schema):
        if entry_schema['type'] == "integer" or entry_schema['type'] == "float" or entry_schema['meta']['database']['type'] == "TIMESTAMP":
            param_schema = {
                'oneof': [
                    {
                        'type': 'list',
                        'schema': {
                            'type': entry_schema['type']
                        }
                    },
                    {
                        'type': entry_schema['type']
                    },
                    {
                        'type': 'dict',
                        'schema': {
                            'min': {
                                'type': entry_schema['type'],
                                'required': True
                            },
                            'max': {
                                'type': entry_schema['type'],
                                'required': True
                            }
                        }
                    },
                    {
                        'type': 'dict',
                        'schema': {
                            'min': {
                                'type': entry_schema['type'],
                                'required': True
                            }
                        }
                    },
                    {
                        'type': 'dict',
                        'schema': {
                            'max': {
                                'type': entry_schema['type'],
                                'required': True
                            }
                        }
                    }
                ]
            }
        elif entry_schema['type'] == 'dict' and 'codec' in  entry_schema['meta']:
            param_schema = {
                'oneof': [
                    {
                        'type': entry_schema['type']
                    },
                    {
                        'type': 'integer'
                    }
                ]
            }
        else:            
            param_schema = {
                'oneof': [
                    {
                        'type': 'list',
                        'schema': {
                            'type': entry_schema['type']
                        }
                    },
                    {
                        'type': entry_schema['type']
                    }
                ]
            }
        return param_schema


    # Cerberus does not support validation of a top level list
    # https://github.com/pyeve/cerberus/issues/220
    def validate(self, query):
        if isinstance(query, list):
            for q in query:
                if not self._validator(q):
                    self.errors = self._validator.errors
                    return False 
            return True
        retval = self._validator(query)
        self.errors = self._validator.errors
        return retval


    def normalized(self, query):
        if isinstance(query, list):
            if len(query) == 0: query = [{}]
            for i in range(len(query)): query[i] = self._validator.normalized(query[i])
        else:
            query = self._validator.normalized(query)
        return query


    # This function is used in generating the package documentation
    def create_query_format_json(self):
        json_obj = loads(str(self._validator.schema).replace("'", '"').replace(" True", " true"). replace(" False", " false"))
        with open(join(dirname(__file__), self.table_name + "_query_format.json"), "w") as file_ptr:
            dump(json_obj, file_ptr, indent=4, sort_keys=True)


