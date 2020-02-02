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


# TODO: Get rid of self.data and make explcit members
class genetic_code_entry():


    _logger = getLogger(__name__)


    def __init__(self, iput=[], idx=0, oput=[], genetic_code=None):
        if genetic_code is None:
            self.data = [iput, idx, oput, idx < len(codon_library)]
        else:
            self.data = [genetic_code.entries[0], 
        genetic_code_entry._logger.debug("Created genetic code entry %s", str(self.data))


    def set_input(self, iput):
        self.data[0] = [] if iput is None else array(iput, dtype=uint32)
        genetic_code_entry._logger.debug("Set genetic code entry input to %s", str(self.data[0]))


    def set_idx(self, idx):
        self.data[1] = uint32(idx)
        self.data[3] = idx < len(codon_library)
        genetic_code_entry._logger.debug("Set genetic code entry idx to %s & codon to %s", str(self.data[1]), self.data[3])


    def set_output(self, oput):
        self.data[2] = [] if oput is None else array(oput, dtype=float32)
        genetic_code_entry._logger.debug("Set genetic code entry output to %s", str(self.data[2]))


    def get_input(self):
        genetic_code_entry._logger.debug("Genetic code entry input is %s ", str(self.data[0]))
        return self.data[0]


    def get_idx(self):
        genetic_code_entry._logger.debug("Genetic code entry idx is %d ", self.data[1])
        return self.data[1]


    def get_output(self):
        genetic_code_entry._logger.debug("Genetic code entry input is %s ", str(self.data[2]))
        return self.data[2]


    def get_name(self):
        return codon_library[self.data[3]].name if self.is_codon() else 'code ' + str(self.data[3])


    def is_codon(self):
        return self.data[3]


    def is_input(self):
        return self.data[1] == 0


    def is_output(self):
        return self.data[1] == 1


    def append_input(self, iput):
        if self.data[0] is None:
            self.set_input(iput)
        else:
            self.data[0] = concatenate(self.data[0], array(iput, dtype=uint32))


    def append_output(self, oput):
        if self.data[2] is None:
            self.set_output(oput)
        else:
            self.data[2] = concatenate(self.data[2], array(oput, dtype=float32))


    def modify_input(self, idx, iput):
        for i in idx: self.data[0][i] = array(iput, dtype=uint32)
        

    def modify_output(self, idx, oput):
        for i in idx: self.data[0][i] = array(oput, dtype=float32)


    def len_input(self, x=None):
        return self.data[0].shape[0] if x is None else self.data[0][x].shape[0]


    def len_output(self):
        return self.data[2].shape[0]


    def get_random_input_index(self):
        return randint(self.len_input())


    def get_random_output_index(self):
        return randint(self.len_output())


