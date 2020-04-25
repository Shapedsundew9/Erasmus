'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/entry_column_meta_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Saturday, April 25th 2020, 5:33:07 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from cerberus import Validator
from os.path import dirname, join
from json import load


__ENTRY_COLUMN_META_SCHEMA = schema = load(open(join(dirname(__file__), "entry_column_meta_format.json"), "r"))


class __entry_column_meta_validator(Validator):


    def _check_with_valid_immutable(self, field, value):
        if value and "location" in self.document and len(self.document["location"]) != 1:
            self._error(field, "Immutable fields can only be defined in one location.")


    def _check_with_valid_compressed(self, field, value):
        if value and "database" in self.document and "type" in self.document["database"]:
            if self.document["database"]["type"] != "BYTEA":
                self._error(field, "A field must be of BYTEA type to be compressed.")


    def _check_with_valid_sha256(self, field, value):
        if value and "database" in self.document and "type" in self.document["database"]:
            if self.document["database"]["type"] != "BYTEA":
                self._error(field, "A field must be of BYTEA type to be an SHA256.")
        if value and "compressed" in self.document and self.document["compressed"]: 
            self._error(field, "A SHA256 field cannot be compressed.")


entry_column_meta_validator = __entry_column_meta_validator(__ENTRY_COLUMN_META_SCHEMA)
entry_column_meta_validator.allow_unknown = True
