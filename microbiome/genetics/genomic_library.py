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
from .genomic_library_store import genomic_library_store as store
from logging import getLogger
from .entry_validator import entry_validator, ENTRY_VALIDATION_SCHEMA
from .query_validator import query_validator
from pprint import pprint, pformat
from copy import deepcopy


# The genomic_library is responsible for:
#   1. Persisting entries
#   2. Converting entries from application format to storage format
#   3. Converting entries from storage format to application format
#   4. Populating calculable entry fields
#   4. Validating entries to be added to the store
#   5. Retrieving entries based on criteria
class genomic_library():


    __store = None
    __entry_validator = entry_validator(ENTRY_VALIDATION_SCHEMA)
    __logger = getLogger(__name__)


    def __init__(self):
        if genomic_library.__store is None: genomic_library.__store = store()
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
        genomic_library.__store.store(entry, settime=False)


    # Return an application formatted entry from the store
    def __getitem__(self, signature):
        return self.__application_format(genomic_library.__store[signature])


    # Return a list of application formatted entries from the store that meet the query
    def load(self, query, fields=["*"]):
        valid, errors = query_validator(query)
        if not valid:
            genomic_library.__logger.warning("Query is not valid:\n%s\n%s", pformat(errors), pformat(query))
            return []
        entries = genomic_library.__store.load(fields, query)
        for i in range(len(entries)): entries[i] = self.__application_format(entries[i])
        return entries


    # Store a new application formatted entry.
    def store(self, entry):
        if self.validate(entry):
            new_entry = genomic_library.__entry_validator.normalized(entry)
            if self.__calculate_fields(new_entry):
                genomic_library.__store.store(self.__storage_format(new_entry))
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
        gca = genomic_library.__store[entry['gca']]
        if gca is None: genomic_library.__logger.warning("gca %s does not exist.",entry['gca'])
        gcb = genomic_library.__store[entry['gcb']]
        if gcb is None: genomic_library.__logger.warning("gcb %s does not exist.",entry['gcb'])
        if gca is None or gcb is None: return False
        entry['code_depth'] = max((gca['code_depth'], gcb['code_depth'])) + 1
        entry['num_codes'] = gca['num_codes'] + gcb['num_codes']
        entry['raw_num_codons'] = gca['raw_num_codons'] + gcb['raw_num_codons']
        entry['generation'] = max((gca['generation'], gcb['generation'])) + 1
        entry['properties'] = self.__properties_application_format(gca['properties'] | gcb['properties'])
        return True


    # Must be able to process entries that only contain a subset of fields
    def __application_format(self, store_entry):
        entry = deepcopy(store_entry)
        for k, v in ENTRY_VALIDATION_SCHEMA.items():
            if v['meta']['compressed']: entry[k] = loads(decompress(store_entry[k]))
            if v['meta']['sha256']: entry[k] = store_entry[k].hex() 
        entry['properties'] = self.__properties_application_format(store_entry['properties'])
        return entry


    def __storage_format(self, application_entry):
        # A lot of fields require no change of format
        entry = deepcopy(application_entry)
        for k, v in ENTRY_VALIDATION_SCHEMA.items():
            if v['meta']['compressed']: entry[k] = compress(dumps(application_entry[k]), 9)
            if v['meta']['sha256']: entry[k] = bytearray.fromhex(application_entry[k]) 
        entry['properties'] = self.__properties_storage_format(application_entry['properties'])
        return entry


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