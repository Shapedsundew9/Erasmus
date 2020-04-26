'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:33:43 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from zlib import compress, decompress
from pickle import dumps, loads
from numpy.random import randint
from .database_table import database_table
from logging import getLogger
from .genomic_library_entry_validator import genomic_library_entry_validator, ENTRY_VALIDATION_SCHEMA
from .query_validator import query_validator
from pprint import pprint, pformat
from copy import deepcopy
from .config import get_config


__TABLE_NAME = "genomic_library"

# The genomic_library is responsible for:
#   1. Persisting entries
#   2. Converting entries from application format to storage format
#   3. Converting entries from storage format to application format
#   4. Populating calculable entry fields
#   4. Validating entries to be added to the store
#   5. Retrieving entries based on criteria
class genomic_library():


    __store = None
    __query_validator = query_validator(ENTRY_VALIDATION_SCHEMA, __TABLE_NAME)
    __entry_validator = genomic_library_entry_validator(ENTRY_VALIDATION_SCHEMA)
    __logger = getLogger(__name__)


    def __init__(self):
        if genomic_library.__store is None:
            genomic_library.__store = database_table(genomic_library.__logger, __TABLE_NAME,
                get_config(["data_stores", __TABLE_NAME]), ENTRY_VALIDATION_SCHEMA)
        if not len(genomic_library.__store): self.__entry_zero()


    def __entry_zero(self):
        entry = {}
        for k, v in ENTRY_VALIDATION_SCHEMA.items():
            if v['meta']['database']['type'] == "BYTEA":
                value = b'\x00' * (v['minlength'] // 2) if "minlength" in v else b'\x00'
            elif v['meta']['database']['type'] == "INTEGER" or v['meta']['database']['type'] == "BIGINT":
                value = 0
            elif v['meta']['database']['type'] == "TIMESTAMP":
                value = "2000-01-01T00:00:00.000001Z" 
            elif v['meta']['database']['type'] == "REAL":
                value = 0.0
            else:
                value = "entry_zero"
            entry[k] = value
        genomic_library.__store.store(entry)


    # Return an application formatted entry from the store
    def __getitem__(self, signature):
        value = genomic_library.__store.load([{"signature": signature}])
        return None if value is None else value[0]


    # Return a list of application formatted entries from the store that meet the query
    def load(self, query, fields=None):
        valid, errors = genomic_library.__query_validator.validate(query)
        if not valid:
            genomic_library.__logger.warning("Query is not valid:\n%s\n%s", pformat(errors), pformat(query))
            return []
        genomic_library.__query_validator.normalized(query)
        return genomic_library.__store.load(fields, query)


    # Store a new application formatted entry.
    def store(self, entry):
        if self.validate(entry):
            new_entry = genomic_library.__entry_validator.normalized(entry)
            if self.__calculate_fields(new_entry):
                genomic_library.__store.store(new_entry)
                return new_entry
        return None


    # Validates an application format entry and populates fields that do not
    # require store lookups to calculate.
    def validate(self, entry):
        if not genomic_library.__entry_validator(entry):
            err_txt = genomic_library.__entry_validator.errors
            genomic_library.__logger.warning("Entry is not valid:\n%s\n%s", pformat(err_txt), pformat(entry))
            return False
        return True


    def __calculate_fields(self, entry):
        # TODO: Need to update gca & gcb if necessary.
        gca = self[entry['gca']]
        if gca is None: genomic_library.__logger.warning("gca %s does not exist.",entry['gca'])
        gcb = self[entry['gcb']]
        if gcb is None: genomic_library.__logger.warning("gcb %s does not exist.",entry['gcb'])
        if gca is None or gcb is None: return False
        entry['code_depth'] = max((gca['code_depth'], gcb['code_depth'])) + 1
        entry['num_codes'] = gca['num_codes'] + gcb['num_codes']
        entry['raw_num_codons'] = gca['raw_num_codons'] + gcb['raw_num_codons']
        entry['generation'] = max((gca['generation'], gcb['generation'])) + 1
        entry['properties'] = gca['properties']
        for k, v in gcb['properties']:
            if k in entry['properties']: entry['properties'][k] = entry['properties'][k] or v
        return True


    def __properties_application_format(self, storage_properties):
        properties = {}
        for k, v in ENTRY_VALIDATION_SCHEMA['properties']['meta']['codec'].items():
            properties[k] = bool(storage_properties & 1 << v)
        return properties


    def __properties_storage_format(self, application_properties):
        properties = 0x0000000000000000
        for k, v in ENTRY_VALIDATION_SCHEMA['properties']['meta']['codec'].items():
            if k in application_properties and application_properties[k]: properties |= 1 << v
        return properties


    def __len__(self):
        return len(genomic_library.__store)