'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation_replicate.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 8:53:18 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from copy import deepcopy
from .mutation_base import mutation_base


# Do nothing
class mutation_trg000(mutation_base):

    def __init__(self, weight=0.01):
        super().__init__('replicate', weight)
        self.code = 'trg000'
        

    def mutate(self, code, partners=None):
        return None
        