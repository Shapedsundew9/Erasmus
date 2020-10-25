'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/entry_column_meta_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Saturday, April 25th 2020, 5:33:07 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from cerberus import Validator
from datetime import datetime
from hashlib import sha256
from json import load
from os.path import dirname, join


with open(join(dirname(__file__), "formats/work_log_entry_format.json"), "r") as file_ptr:
    _WORK_LOG_ENTRY_SCHEMA = schema = load(file_ptr)


class _work_log_validator(Validator):

    def _check_with_valid_created(self, field, value):
        try:
            date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            self._error(field, "Created date-time is not valid. Unknown error parsing.")
            return

        if date_time_obj > datetime.utcnow():
            self._error(field, "Created date-time cannot be in the future.")


    def _normalize_default_setter_set_created(self, document):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


work_log_validator = _work_log_validator(_WORK_LOG_ENTRY_SCHEMA)