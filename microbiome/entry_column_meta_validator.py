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


with open(join(dirname(__file__), "formats/entry_column_meta_format.json"), "r") as file_ptr:
    _ENTRY_COLUMN_META_SCHEMA = schema = load(file_ptr)


class _entry_column_meta_validator(Validator):


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


    def _check_with_valid_codec(self, field, value):
        if value and "database" in self.document and "type" in self.document["database"]:
            if not self.document["database"]["type"] in ("INTEGER", "BIGINT"):
                self._error(field, "A field must be of an integer type to have a codec.")
            size = 32 if self.document["database"]["type"] == "INTEGER" else 64
            for v in value.values():
                if v >= size: self._error(field, "Bit index must be within the size of the type (< %d)", size)
            if len(list(value.values())) != len(set(value.values())):
                self._error(field, "Bit indices cannot be duplicated in a codec.")
            if self.document['sha256']: self._error(field, "A codec cannot be an SHA256.")
            if self.document['compressed']: self._error(field, "A codec cannot be compressed.")


    def _check_with_valid_cumsum(self, field, value):
        if value:
            if self.document['type'] in ("VARCHAR", "TIMESTAMP", "SMALLSERIAL", "SERIAL", "BIGSERIAL"):
                self._error(field, "To have a cumulative sum the type must be NUMERIC but not SERIAL.")


entry_column_meta_validator = _entry_column_meta_validator(_ENTRY_COLUMN_META_SCHEMA)
entry_column_meta_validator.allow_unknown = True
