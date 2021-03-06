'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:30 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''

from numpy.random import choice
from numpy import array, sum
from .genetic_code import genetic_code
from .genomic_library import genomic_library
from .codon_library import codon_library
from .mutations import mutation_rig000, mutation_trg000, mutation_rmi000
from .memory import memory
from .gene import gene
from logging import getLogger
from sys import exc_info
from time import time


# An agent is a recursive structure of genetic_codes wrapped up in a gene
class agent():


    _logger = getLogger(__name__)
    _mutation_list = (
        mutation_rig000(),
        mutation_trg000(),
        mutation_rmi000()
    )
    _mutation_weights = array([m.weight for m in _mutation_list])
    _mutation_distribution = _mutation_weights / sum(_mutation_weights)
    glib = genomic_library()


    # The default gene only has an input codon and an output codon
    def __init__(self, base_gene=None):
        # TODO: Add a weight based random code option
        self._gene = gene() if base_gene is None else base_gene
        self._memory = memory()


    def exec(self, d=array([])):
        return self._gene.exec(d, self._memory)


    def is_alive(self):
        try:
            self.exec()
        except:
            agent._logger.debug("Agent still born with %s", exc_info()[0])
            return False
        return True


    def add_code_to_library(self, meta_data=None):
        return self._gene.add_code_to_library(meta_data)


    def get_code(self, eid):
        return self._gene.genetic_code


    def reproduce(self, partners=None, attempts=100):
        agent._logger.debug("Agent reproduction starting:")
        start = time()

        # TODO: Test is_alive in fitness function - wastes too much time here.
        for a in range(attempts):
            draw = choice(len(self._mutation_list), p=self._mutation_distribution)
            offspring = agent(gene(self._mutation_list[draw].mutate(self._gene.genetic_code, partners)))
            if not offspring is None and offspring.is_alive():
                stop = time()
                agent._logger.debug("Agent reproduced in %d attempts in %0.4fs.", a + 1, stop - start)
                return offspring
        stop = time()
        agent._logger.debug("Agent failed to reproduce in %d attempts in %0.4fs.", attempts, stop - start)        
        return None
