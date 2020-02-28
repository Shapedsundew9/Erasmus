'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation_insert_gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 9:00:48 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from ..genomic_library import genomic_library
from .mutation_base import mutation_base
from ..genetic_code import genetic_code
from copy import deepcopy
from logging import getLogger


# Insert a random genetic_code from the genomic library at a random position
# Append new code inputs to inputs
# Append new code outputs to outputs
class mutation_rig000(mutation_base):

    _glib = genomic_library()
    _logger = getLogger(__name__)


    def __init__(self, weight=1.0):
        super().__init__('replicate', weight)
        self.code = 'rig000'


    def _insert(self, new_code, new_entry, index):
        return super()._insert(new_code, new_entry, index)


    def mutate(self, code, partners=None):
        # Create a clone and determine code to insert & position.
        index = code.random_index()
        new_code = code.clone()
        new_entry = genetic_code(library_entry=self._glib.random_entry()).make_entry()

        # B'zinga
        return self._insert(new_code, new_entry, index)


        