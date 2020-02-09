'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from .genetic_code import genetic_code
from .codon_library import codon_library
from .genomic_library import genomic_library


# gene() is a wrapper to a genetic_code that makes it executable.
# This layer is abstracted as there are opportunities for optimisation and caching
# of genes to increase performance.
class gene():


    _glib = genomic_library()


    # seed is a genetic_code or an index to one
    def __init__(self, gc=None):
            self.genetic_code = genetic_code() if gc is None else gc 


    def exec(self, d=None, m=None):
        for i, g in enumerate(self.genetic_code.entries[:-1], 1):
            output = codon_library[g.get_idx()].exec(d, m) if g.is_codon() else gene(self._glib[g.get_idx()]).exec(d, m)
            g.set_output(output)
            d = genetic_code.get_inputs(i)
        return d
