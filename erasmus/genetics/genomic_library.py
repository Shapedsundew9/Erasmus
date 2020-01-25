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
from .codon_library import codon_library
from .genetic_code import genetic_code


# TODO: Add statistics to code entries.
class genomic_library():

    name = None
    _store = None

    def __init__(self, name='genomic_library'):
        if self.name is None:
            self.name = name
            self._store = store(name)

        # In the event the store does not exist an empty one will be created
        # It is then populated with the genes containing just one codon
        if self._store.is_empty:
            for i, c in enumerate(codon_library): self.add_entry(genetic_code(codon_idx=(c, i)).make_library_entry())


    def __getitem__(self, key):
        return self._store.get_by_idx(key)


    def __len__(self):
        return len(self._store)

    
    def add_entry(self, new_entry):
        self._store.add(new_entry)


    def get_entry(self, eid):
        return self._store.get(eid)


    def random_code(self):
        return randint(self.__len__())
