'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from functools import lru_cache
from numpy import array
from numpy.random import randint
from .codon_library import codon_library
from .genetic_code import genetic_code
from .genomic_library import genomic_library
from .genomic_library_entry import genomic_library_entry as entry


# The genetic code is a list of gene/codon references & the connectivity
# entry = [inputs, reference to gene/codon, outputs]
# _entries = [ input_entry, entry0, entry1, entry2, ... entryN, output_entry]
class gene():


    _glib = genomic_library()


    def __init__(self, index=None, random=False):
        if not index is None:
            self._glib[index]
        else:
            self.genetic_code = self._glib.random_code() if random else genetic_code()


    def exec(self, d=None, m=None):
        for i, g in enumerate(self.genetic_code.entries[:-1], 1):
            output = codon_library[g.get_idx()].exec(d, m) if g.is_codon() else self._cache(g.get_idx()).exec(d, m)
            g.set_output(output)
            d = self.get_inputs(i)
        return d


    def get_inputs(self, idx):
        return array([self.genetic_code.entries[i[0]].get_output()[i[1]] for i in self.genetic_code.entries[i].get_input()])


    def add_code_to_library(self, meta_data=None):
        self._glib.add_entry(self.genetic_code.make_library_entry())


    @lru_cache(maxsize=1000)
    def _cache(self, index):
        return gene(self._glib[index])