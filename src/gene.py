'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:30 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''


import numpy as np
from geonomic_library import geonomic_library
from copy import deepcopy


class gene():

    # The default gene only has an input codon and an output codon
    def __init__(self):
        self._input_refs = [None, None]
        self._geonomic_refs = np.array([0, 0], np.unit32)
        self._size = len(self._geonomic_refs)


    # The input of the gene is a 1-dimensional np.array(dtype=np.float32)
    def exec(self, in_data):
        if in_data.shape[0] < self._size: raise Exception('Gene interface', 'Too few input parameters')
        outputs = [None] * self._size
        outputs[0] = in_data  

        for g in range(1, self._size):
            if outputs[g] is None: self._exec_gene(g, outputs)
        
        return outputs[-1]


    def _exec_gene(self, g, outputs):
        inputs = []
        for r in self._input_refs:
            if outputs[r[0]] is None: self._exec_gene(r[0], outputs)
            inputs.append(outputs[r[0]])
        outputs[g] = geonomic_library[self._geonomic_refs[g]](np.array(inputs).flatten())


    def replicate(self, mutate=True):
        if not mutate: return deepcopy(self)

