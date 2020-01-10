'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:33:43 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from .genomic_library_entry import genomic_library_entry as entry
from .genomic_library_store import genomic_library_store as store
from .codon_library import codon_library
from .genetic_code import genetic_code


class genomic_library():

    def __init__(self, name='genomic_library'):
        self.name = name
        self._store = store(name)

        # In the event the store does not exist an empty one will be created
        # It is then populated with the genes containing just one codon
        if self._store.is_empty:
            for i, c in enumerate(codon_library): self.add_code(genetic_code(codon_idx=(c, i)))


    def __len__(self):
        return len(self._store)


    def add_code(self, code, meta_data=None):
        new_entry = entry(code.zserialise(), code.id(), code.ancestor, code.name, meta_data)
        self.add_entry(new_entry)


    def get_code(self, id):
        entry = self.get_entry(id)
        code = genetic_code(entry.name, entry.ancestor)
        code.zdeserialise(entry.data)
        return code

    
    def add_entry(self, new_entry):
        self._store.add(new_entry)


    def get_entry(self, id):
        return self._store.get(id)



