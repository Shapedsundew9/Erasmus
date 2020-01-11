'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:30 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''


from .genetic_code import genetic_code
from .genomic_library import genomic_library
from .codon_library import codon_library


# A gene is a recursive structure of other genes
class agent():

    # The default gene only has an input codon and an output codon
    def __init__(self):
        self._code = genetic_code()
        self._library = genomic_library()


    def exec(self, d):
        for i, g in enumerate(self._code[:-1], 1):
            output = codon_library[g.get_idx()].exec(d) if g.is_codon() else self._library[g.get_idx()].exec(d)
            g.set_output(output)
            d = self._code.get_inputs(i)
        return d


    def reproduction(self, partner=None):
..to be continued