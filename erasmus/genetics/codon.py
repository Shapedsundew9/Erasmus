'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:24 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''


from inspect import signature
from logging import getLogger
from numpy import append, zeros, int32, array, float32


class codon():


    _logger = getLogger(__name__)


    def __init__(self, func, name, desc=None, isMemory=False, isConstant=False, isIO=False):
        self.func = func
        self.name = name
        self.desc = desc
        self.isMemory = isMemory
        self.isConstant = isConstant
        self.isIO = isIO
        

    def exec(self, d, m, output=None):
        #codon._logger.debug("Executing %s codon with parameters %s", self.name, str(d))
        if self.isConstant: return array(output)
        if self.isIO: return d
        if self.isMemory: return self.func(m, *d)
        return array([self.func(*d)], dtype=float32)