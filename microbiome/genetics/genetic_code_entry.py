'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genetic_code_entry.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 11:58:27 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from .codon_library import codon_library
from numpy import array, int32, uint32, float32, concatenate
from numpy.random import randint
from logging import getLogger
from more_itertools import pairwise


class ref():

    def __init__(self, row=0, pos=0):
        self.row = uint32(row)
        self.pos = uint32(pos)


    def __str__(self):
        return str((self.row, self.pos))


class inputs(list):

    def __init__(self, *args, s=None):
        if s is None:
            super()._init_(*args)
        else:
            super()._init_([ref() for _ in range(s)])

    def __str__(self):
        ref_str = '('
        for r in self: ref_str += str(r) 
        return str(len(self)) + ',' + ref_str + ')'


class outputs(list):

    def __init__(self, *args, s=None):
        if s is None:
            super()._init_(*args)
        else:
            super()._init_([float32(0)] * s)

    def __str__(self):
        val_str = '['
        for v in self: val_str += str(v) + ', '
        return str(len(self)) + ',' + val_str + ']'


# TODO: Get rid of self.data and make explcit members
class genetic_code_entry():


    _logger = getLogger(__name__)


    def __init__(self, iput=None, signature=None, is_codon=False, oput=None, genetic_code=None):
        if genetic_code is None:
            if iput is None: iput = inputs()
            if oput is None: oput = outputs()
            self.input = iput if isinstance(iput, inputs) else inputs(iput)
            self.idx = uint32(idx)
            self.output = oput if isinstance(oput, outputs) else outputs(oput)
            self.is_codon = is_codon
            self.name = codon_library[self.idx].name if is_codon else None
        else:
            self.input = genetic_code.entries[0].input
            self.idx = uint32(genetic_code.idx)
            self.output = genetic_code.entries[-1].output
            self.is_codon = len(genetic_code.entries) == 1
            self.name = genetic_code.name

        genetic_code_entry._logger.debug("Created genetic code entry %s", str(self))


    def __str__(self):
        return str(self.input) + ':' + str(self.idx) + ':' + str(self.name) + ':' + str(self.output) + ':' + str(self.is_codon)


    def num_inputs(self):
        return len(self.input)


    def num_outputs(self):
        return len(self.output)


    def is_input_entry(self):
        return self.idx == 0


    def is_output_entry(self):
        return self.idx == 1


    def set_output(self, o):
        assert(o.shape[0] == len(self.output))
        self.output = outputs(o)



