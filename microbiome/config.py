'''
Filename: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client/genetics/config.py
Path: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client/genetics
Created Date: Tuesday, February 25th 2020, 6:17:46 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from .entry_column_meta_validator import entry_column_meta_validator
from cerberus import Validator, SchemaError
from logging import getLogger
from os.path import isfile, dirname, join
from json import load, dump


config = None
__logger = getLogger(__name__)


class __config_validator(Validator):


    def _check_with_valid_format_file(self, field, value):
        value = join(self.document["format_file_folder"], value) if "format_file_folder" in self.document else join(dirname(__file__), 'formats', value)
        if isfile(value):
            try:
                schema = load(open(value, "r"))
            except Exception as ex:
                self._error(field, "Format file is not valid JSON: {}".format(ex))
                return

            for k, v in schema.items():
                if not 'meta' in v:
                    self._error(field, "No 'meta' key found in {}.".format(k))
                elif not entry_column_meta_validator(v['meta']):
                    self._error(field, "'meta' field format error in {}: {}".format(k, str(entry_column_meta_validator.errors)))
        else:
            self._error(field, "Format file {} not found.".format(value))

           
def set_config(new_config):
    global config
    config = new_config
    validate_config()
    return config


def validate_config():
    global config
    v = __config_validator(load(open(join(dirname(__file__), "formats/config_format.json"), "r")))
    v.allow_unknown = True
    if not v.validate(config):
        __logger.error("Config validation failed with error(s) %s", str(v.errors))
        exit(1)
    config = v.normalized(config)

    # Populate the database table schemas
    for k, v in config['tables'].items():
        value = v['format_file']
        value = join(v['format_file_folder'], value) if 'format_file_folder' in v else join(dirname(__file__), 'formats', value)
        config['tables'][k]['schema'] = load(open(value, "r"))
        for k, v in config['tables'][k]['schema'].items(): v['meta'] = entry_column_meta_validator.normalized(v['meta'])

    return config


def save_config(config_file_path='config.json'):
    with open(config_file_path, 'w') as file_ptr:
        dump(config, file_ptr)


def get_config():
    return config