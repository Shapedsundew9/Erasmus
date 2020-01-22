'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genetic_code_entry.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 11:58:27 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from numpy import array, int32, uint32, float32, concatenate
from numpy.random import randint

# TODO: Get rid of self.data and make explcit members
class genetic_code_entry():

    def __init__(self, iput=None, codon=False, idx=0, oput=0):
        self.data = [iput, idx, oput, codon]


    def set_input(self, iput):
        self.data[0] = None if iput is None else array(iput, dtype=uint32)


    def set_idx(self, idx):
        self.data[1] = uint32(idx)


    def set_output(self, oput):
        self.data[2] = None if oput is None else array(oput, dtype=float32)


    def set_codon(self, c=True):
        self.data[3] = c


    def get_input(self):
        return self.data[0]


    def get_idx(self):
        return self.data[1]


    def get_output(self):
        return self.data[2]


    def is_codon(self):
        return self.data[3]


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


