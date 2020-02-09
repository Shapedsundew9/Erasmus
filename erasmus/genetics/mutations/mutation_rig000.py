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


# Insert a random genetic_code from the genomic library
class mutation_rig000(mutation_base):

    _glib = genomic_library()

    def __init__(self, weight=1.0):
        super().__init__('replicate', weight)
        self.code = 'rig000'


    def mutate(self, code, partners=None):
        index = code.random_index()
        random_code = genetic_code(library_entry=self._glib.random_entry())
        mutation_base._logger.debug("%s inserted genetic code %d in position %d", self.code, random_code, index)
        return deepcopy(code).insert(index, random_code)


        