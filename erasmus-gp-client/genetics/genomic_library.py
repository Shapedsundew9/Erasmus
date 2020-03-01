'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:33:43 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from numpy.random import randint
from .genomic_library_entry import genomic_library_entry as entry
from .genomic_library_store import genomic_library_store as store
from logging import getLogger


# The genomic_library is responsible for:
#   1. Persisting entries
#   2. Converting entries from application format to storage format
#   3. Converting entries from storage format to application format
#   4. Populating calculable entry fields
#   4. Validating entries to be added to the store
#   5. Retrieving entries based on criteria
class genomic_library():


    _store = None
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library._store is None: genomic_library._store = store()


    def __getitem__(self, signature):
        return self._application_format(genomic_library._store[signature])


    def __setitem__(self, signature, entry):
        storage_format_entry = self._storage_format(entry)
        if not storage_format_entry is None: genomic_library._store[signature] = storage_format_entry
        return 


    def __len__(self):
        return len(genomic_library._store)


    def get_random_entry(self):
        # Never select the input or output codon
        return self[randint(self.__len__() - 2) + 2]


# Instance of the genomic_library
glib = genomic_library()