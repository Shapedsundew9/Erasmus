'''
Filename: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client/genetics/config.py
Path: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client/genetics
Created Date: Tuesday, February 25th 2020, 6:17:46 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from cerberus import Validator
from logging import getLogger
from yaml import safe_load, YAMLError, dump
from os.path import isfile


config = None
_logger = getLogger(__name__)
_schema = {
    'local_genomic_library': {
        'type': dict,
        'schema': {
            'dbname': {'type': 'string', 'default': 'default'},
            'recreate': {'type': 'boolean', 'default': False},
            'temp': {'type': 'boolean', 'default': False},
            'host': {'type': 'string', 'default': 'localhost'},
            'username': {'type': 'string', 'default': 'postgres'},
            'password': {'type': 'string', 'default': 'postgres'},
            'port': {'type': 'integer', 'default': 5432, 'min': 1024, 'max': 65535}
        }
    }
}


def load_config(config_file_path='config.yaml'):
    global config
    v = Validator(_schema)
    if isfile(config_file_path):
        with open(config_file_path) as file_ptr:
            try:
                config = safe_load(file_ptr)
            except YAMLError as ex:
                _logger.warn("YAML could not parse config file %s with error %s", config_file_path, str(ex))
                config = None
        if not v.validate(config):
            _logger.warn("Config %s validation failed with error(s) %s", config_file_path, str(v.errors))
            config = None
    else:
        _logger.warn("Config file %s not found.", config_file_path)
    return config


def save_config(config_file_path='config.yaml'):
    with open(config_file_path, 'w') as file_ptr:
        dump(config, file_ptr)


def get_config(section, param_list):
    return (config[section][param] for param in param_list)


def _save_config_validation_schema(config_validation_file_path='config_validation.yaml'):
    with open(config_validation_file_path, 'w') as file_ptr:
        dump(_schema, file_ptr)
