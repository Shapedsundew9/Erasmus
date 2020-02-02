'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:24 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''


from inspect import signature
from logging import getLogger
from numpy import append, zeros, int32


class codon():


    _logger = getLogger(__name__)


    def __init__(self, func, name, desc=None, isMemory=False):
        self.func = func
        self.name = name
        self.desc = desc
        self.isMemory = isMemory
        

    def exec(self, d, m):
        codon._logger.debug("Executing %s codon with parameters %s", self.name, str(d))
        if not callable(self.func): return self.func
        num_params = len(signature(self.func).parameters)
        if d is None: d = zeros((num_params), dtype=int32)
        if d.shape[0] < num_params: d = append(d, [0] * (num_params - d.shape[0]))
        if self.isMemory: return self.func(m, *d[0:num_params - 1])
        return self.func(*d[0:num_params])