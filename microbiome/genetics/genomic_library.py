'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:33:43 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from numpy.random import randint
from .genomic_library_store import genomic_library_store as store
from logging import getLogger
from .validation import create_validator
from pprint import pprint


# The genomic_library is responsible for:
#   1. Persisting entries
#   2. Converting entries from application format to storage format
#   3. Converting entries from storage format to application format
#   4. Populating calculable entry fields
#   4. Validating entries to be added to the store
#   5. Retrieving entries based on criteria
class genomic_library():


    _store = None
    _validator, _schema = create_validator()
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library._store is None: genomic_library._store = store()


    # Return an application formatted entry from the store
    def __getitem__(self, signature):
        return self._application_format(genomic_library._store[signature])


    # Return an application formatted entry from the store
    def get_gc(self, signature):
        return self[signature]


    # Store a new application formatted entry. Return true if the entry is added.
    def set_gc(self, entry):
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


    def _calculate_fields(entry):
        gca = genomic_library._store.get_limited(entry['GCA'])
        gcb = genomic_library._store.get_limited(entry['GCB'])
        if gca is None or gcb is None: return False
        entry['code_depth'] = max((gca['code_depth'], gcb['code_depth'])) + 1
        entry['num_codes'] = gca['num_codes'] + gcb['num_codes']
        entry['raw_num_codons'] = gca['raw_num_codons'] + gcb['raw_num_codons']
        entry['generation'] = max((gca['generation'], gcb['generation'])) + 1
        for         




    def __len__(self):
        return len(genomic_library._store)


    def get_random_entry(self):
        # Never select the input or output codon
        return self[randint(self.__len__() - 2) + 2]


# Instance of the genomic_library
glib = genomic_library()