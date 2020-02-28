'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation_replicate.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 8:53:18 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from copy import deepcopy
from .mutation_base import mutation_base
from .mutation_rig000 import mutation_rig000


# Duplicate the exiting code
class mutation_trg000(mutation_base):

    def __init__(self, weight=0.01):
        super().__init__('replicate', weight)
        self.code = 'trg000'


    def _insert(self, new_code, new_entry, index):
        return super()._insert(new_code, new_entry, index)
       

    def mutate(self, code, partners=None):
        return self._insert(code.mono_code(), code.make_entry(), 1)
        