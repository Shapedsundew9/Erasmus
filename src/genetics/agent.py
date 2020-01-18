'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:30 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''

from numpy.random import choice
from numpy import array
from .genetic_code import genetic_code
from .genomic_library import genomic_library
from .codon_library import codon_library
from .mutations import mutation_rig000, mutation_trg000


# An agent is a recursive structure of genetic_codes
class agent():

    _mutation_list = (
        mutation_rig000(),
        mutation_trg000()
    )
    _mutation_distribution = array([m.weight for m in _mutation_list])
    glib = genomic_library()

    # The default gene only has an input codon and an output codon
    def __init__(self, code=None, random_code=False):
        # TODO: Add a weight based random code option
        if code is None and random_code:
            self._code = self.glib.random_code()
        elif code is None: self._code = genetic_code()


    def exec(self, d=None):
        for i, g in enumerate(self._code[:-1], 1):
            output = codon_library[g.get_idx()].exec(d) if g.is_codon() else self.glib[g.get_idx()].exec(d)
            g.set_output(output)
            d = self._code.get_inputs(i)
        return d


    def is_alive(self):
        try:
            self.exec()
        except:
            return False
        return True


    def reproduce(self, partners=None, attempts=100):
        draw = choice(len(self._mutation_list), p=self._mutation_distribution)
        for _ in range(attempts):
            offspring = agent(self._mutation_list[draw].mutate(self._code, partners))
            if offspring.is_alive(): return offspring
        return None
