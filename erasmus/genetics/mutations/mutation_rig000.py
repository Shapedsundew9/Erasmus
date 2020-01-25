'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation_insert_gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 9:00:48 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from ..genomic_library import genomic_library
from .mutation_base import mutation_base
from copy import deepcopy


class mutation_rig000(mutation_base):

    glib = genomic_library()

    def __init__(self, weight=1.0):
        super().__init__('replicate', weight)
        self.code = 'rig000'


    def mutate(self, code, partners=None):
        return deepcopy(code).insert(code.random_index(), self.glib.random_code())


        