'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation_insert_gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Saturday, February 15th 2020, 4:35:08 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from ..genomic_library import genomic_library
from .mutation_base import mutation_base
from ..genetic_code import genetic_code
from ..genetic_code_entry import ref
from copy import deepcopy
from logging import getLogger
from numpy.random import randint
from random import choice


# Find a random input reference from anywhere but the input entry and randomly
# reconnect it to the output of an entry above (closer to the input)
class mutation_rmi000(mutation_base):

    _glib = genomic_library()
    _logger = getLogger(__name__)


    def __init__(self, weight=10.0):
        super().__init__('Rewire', weight)
        self.code = 'rmi000'


    def mutate(self, code, partners=None):
        a = ref(row=randint(1, len(code.entries)))
        if not len(code.entries[a.row].input): return code
        new_code = code.clone()
        a.pos = randint(len(code.entries[a.row].input))
        new_code.entries[a.row].input[a.pos] = choice([ref(i, p) for i, e in enumerate(code.entries[:a.row]) for p in range(len(e.output))])
        return new_code
