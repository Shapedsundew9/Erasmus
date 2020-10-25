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


with open(join(dirname(__file__), "formats/platform_info_entry_format.json"), "r") as file_ptr:
    _PLATFORM_INFO_ENTRY_SCHEMA = schema = load(file_ptr)


class _platform_info_validator(Validator):

    def _check_with_valid_created(self, field, value):
        try:
            date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            self._error(field, "Created date-time is not valid. Unknown error parsing.")
            return

        if date_time_obj > datetime.utcnow():
            self._error(field, "Created date-time cannot be in the future.")


    def _normalize_default_setter_set_signature(self, document):
        sig_str = self.document['machine'] + self.document['processor'] + self.document['python_version']
        sig_str += self.document['system'] + self.document['release'] + str(int(self.document['EGPOps/s']))

        # Remove spaces etc. to give some degrees of freedom in formatting and
        # not breaking the signature
        return sha256("".join(sig_str.split()).encode()).hexdigest()


    def _normalize_default_setter_set_created(self, document):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


    def _coerce_string(self, value, length):
        return value[:length] if isinstance(value, str) and len(value) > length else value
        

    def _normalize_coerce_string_64(self, value):
        return self._coerce_string(value, 64)
        

    def _normalize_coerce_string_128(self, value):
        return self._coerce_string(value, 128)
        

    def _normalize_coerce_string_1024(self, value):
        return self._coerce_string(value, 1024)


platform_info_validator = _platform_info_validator(_PLATFORM_INFO_ENTRY_SCHEMA)