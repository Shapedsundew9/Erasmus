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
from .entry_validator import entry_validator
from pprint import pprint
from copy import deepcopy


_COMPRESSED_FIELDS = ("graph", "meta_data")
_SHA256_FIELDS = ("signature", "GCA", "GCB", "creator")
_PROPERTY_MASKS = (
                    ("extended",     1 <<  0),
                    ("mathematical", 1 <<  8),
                    ("logical",      1 <<  9),
                    ("conditional",  1 << 10)
)


# The genomic_library is responsible for:
#   1. Persisting entries
#   2. Converting entries from application format to storage format
#   3. Converting entries from storage format to application format
#   4. Populating calculable entry fields
#   4. Validating entries to be added to the store
#   5. Retrieving entries based on criteria
class genomic_library():


    _store = None
    _validator = entry_validator()
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library._store is None: genomic_library._store = store()


    # Return an application formatted entry from the store
    def __getitem__(self, signature):
        return self._application_format(genomic_library._store[signature])


    # Return an application formatted entry from the store
    def load_gc(self, signature):
        return self[signature]


    # Store a new application formatted entry. Return true if the entry is added.
    def store_gc(self, entry):
        if self.validate(entry):
            if self._calculate_fields(entry):
                return genomic_library._store.store(self._storage_format(entry))
        return False


    # Validates an application format entry and populates fields that do not
    # require store lookups to calculate.
    def validate(self, entry):
        if not genomic_library._validator(entry):
            err_txt = genomic_library._validator.errors
            genomic_library._logger.warn("Entry is not valid:\n%s\n%s",pprint.pformat(err_txt), pprint.pformat(entry))
            return False
        return True


    def _calculate_fields(self, entry):
        # TODO: Need to update gca & gcb if necessary.
        gca = genomic_library._store.get_limited(entry['GCA'])
        if gca is None: genomic_library._logger.warn("GCA %s does not exist.",entry['GCA'])
        gcb = genomic_library._store.get_limited(entry['GCB'])
        if gcb is None: genomic_library._logger.warn("GCB %s does not exist.",entry['GCB'])
        if gca is None or gcb is None: return False
        entry['code_depth'] = max((gca['code_depth'], gcb['code_depth'])) + 1
        entry['num_codes'] = gca['num_codes'] + gcb['num_codes']
        entry['raw_num_codons'] = gca['raw_num_codons'] + gcb['raw_num_codons']
        entry['generation'] = max((gca['generation'], gcb['generation'])) + 1
        for key in genomic_library._validator.schema['classification']['schema'].keys:
            entry['classification'][key] = gca['classification'][key] or gcb['classification'][key]
        return True


    def _application_format(self, store_entry):
        # A lot of fields require no change of format
        entry = deepcopy(store_entry)
        for compressed_field in _COMPRESSED_FIELDS: entry[compressed_field] = loads(decompress(store_entry[compressed_field]))
        for sha256_field in _SHA256_FIELDS: entry[sha256_field] = store_entry[sha256_field].hex()
        entry['properties'] = {}
        for property_key, property_mask in _PROPERTY_MASKS: entry['properties'][property_key] = bool(store_entry['properties'] & property_mask)
        return entry


    def _storage_format(self, application_entry):
        # A lot of fields require no change of format
        entry = deepcopy(application_entry)
        for compressed_field in _COMPRESSED_FIELDS: entry[compressed_field] = compress(dumps(application_entry[compressed_field]), 9).hex()
        entry['properties'] = 0x0000000000000000
        for property_key, property_mask in _PROPERTY_MASKS:
            if property_key in application_entry['properties'] and application_entry['properties'][property_key]: entry['properties'] |= property_mask
        return entry


    def __len__(self):
        return len(genomic_library._store)


# Instance of the genomic_library
glib = genomic_library()