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
from .genetic_code import genetic_code
from .codon_library import codon_library
from .genetic_code import genetic_code
from logging import getLogger


# TODO: Add statistics to code entries.
class genomic_library():


    name = None
    _store = None
    _logger = getLogger(__name__)


    def __init__(self, name=None, recreate=False, temp=False):
        if genomic_library._store is None and not name is None:
            genomic_library.name  = name
            genomic_library._store = store(name, recreate=recreate, temp=temp)
            genomic_library._logger.info("Genomic library created: Name = %s, recreate=%s, temp=%s", name, recreate, temp)

        # In the event the store does not exist an empty one will be created
        # It is then populated with the genes containing just one codon
        if not genomic_library._store is None and self._store.is_empty:
            genomic_library._logger.debug("Populating genomic library with codons.")
            for i, c in enumerate(codon_library): self.add_code(genetic_code(codon_idx=(c, i)))


    def __getitem__(self, key):
        genomic_library._logger.debug("Accessing %s index %d", genomic_library.name, key)
        return entry(*genomic_library._store.get_by_idx(key))


    def __len__(self):
        genomic_library._logger.debug("Accessing %s", self.name)
        return len(genomic_library._store)


    def add_code(self, code, meta_data=None):
        code.idx = self.add_entry(entry(code.zserialise(), code.id(), code.ancestor, code.name, meta_data))
        

    def add_entry(self, new_entry):
        genomic_library._logger.debug("Adding %s entry to %s", new_entry, genomic_library.name)
        new_entry.index = self._store.add(new_entry)
        return new_entry.index


    def get_entry(self, cid):
        return entry(*genomic_library._store.get(cid))


    def random_entry(self):
        # Never select the input or output codon
        return self[randint(self.__len__() - 2) + 2]