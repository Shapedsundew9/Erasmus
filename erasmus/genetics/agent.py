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
from .memory import memory
from .gene import gene


# An agent is a recursive structure of genetic_codes wrapped up in a gene
class agent():

    _mutation_list = (
        mutation_rig000(),
        mutation_trg000()
    )
    _mutation_distribution = array([m.weight for m in _mutation_list])
    glib = genomic_library()


    # The default gene only has an input codon and an output codon
    def __init__(self, base_gene=None, random=False):
        # TODO: Add a weight based random code option
        self._gene = gene(random=random) if base_gene is None else base_gene
        self._memory = memory()


    def exec(self, d=None):
        return self._gene.exec(d, self._memory)


    def is_alive(self):
        try:
            self.exec()
        except:
            return False
        return True


    def add_code_to_library(self, meta_data=None):
        self._gene.add_code_to_library(meta_data)


    def get_code(self, eid):
        return self._gene.genetic_code


    def reproduce(self, partners=None, attempts=100):
        draw = choice(len(self._mutation_list), p=self._mutation_distribution)
        for _ in range(attempts):
            offspring = agent(self._mutation_list[draw].mutate(self._gene.genetic_code, partners))
            if offspring.is_alive(): return offspring
        return None
