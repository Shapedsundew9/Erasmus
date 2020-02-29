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


# TODO: Add statistics to code entries.
class genomic_library():


    _store = None
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library._store is None: genomic_library._store = store()


    def __getitem__(self, key):
        return entry(*genomic_library._store.get_by_idx(key))


    def __len__(self):
        return len(genomic_library._store)


    def add_code(self, code, meta_data=None):
        added, code.idx = self.add_entry(entry(code.zserialise(), code.id(), code.ancestor, code.name, meta_data))
        return added 
        

    # TODO: Verify ancestor details including timestamp is earlier 
    def add_entry(self, new_entry):
        added, new_entry.index = self._store.add(new_entry)
        return added, new_entry.index


    def get_entry(self, cid):
        return entry(*genomic_library._store.get(cid))


    def random_entry(self):
        # Never select the input or output codon
        return self[randint(self.__len__() - 2) + 2]


# Instance of the genomic_library
glib = genomic_library()