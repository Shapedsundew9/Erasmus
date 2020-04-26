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
from os.path import isfile, dirname, join
from json import load


config = None
_logger = getLogger(__name__)


def load_config(config_file_path='config.yaml'):
    global config
    if isfile(config_file_path):
        with open(config_file_path) as file_ptr:
            try:
                config = safe_load(file_ptr)
            except YAMLError as ex:
                # TODO: Is ex json? Can we pretty print it?
                _logger.warn("YAML could not parse config file %s with error %s", config_file_path, str(ex))
                config = None
                return config
        if not validate_config(): _logger.error("Config file: %s", config_file_path)
    else:
        _logger.warn("Config file %s not found.", config_file_path)
    return config


def set_config(new_config):
    global config
    config = new_config
    validate_config()
    return config


def validate_config():
    global config
    # FIXME: Validation rules need sorting out
    v = Validator(load(open(join(dirname(__file__), "config_format.json"), "r")))
    v.allow_unknown = True
    if not v.validate(config):
        _logger.warning("Config validation failed with error(s) %s", str(v.errors))
        return None
    config = v.normalized(config)
    return config


def save_config(config_file_path='config.yaml'):
    with open(config_file_path, 'w') as file_ptr:
        dump(config, file_ptr)


def get_config(section):
    if section is None: return config
    c = config
    for s in section: c = c[s]
    return c