'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


import numpy as np

# The genetic code is a list of gene/codon references & the connectivity
# entry = [inputs, reference to gene/codon, outputs]
# _entries = [ input_entry, entry0, entry1, entry2, ... entryN, output_entry]
class genetic_code():

    def __init__(self):
        # TODO: Optimisation idea: _entries is a list of lists which is very inefficient.
        # Much less RAM can be used by arranging the components into numpy arrays
        # at the cost of construction time CPU.

        # self._entries = [input_entry, output_entry]
        self._entries = [ [None, 0, None], [None, 0, None]]


    def __getitem__(self, key):
        return self._entries[key]


    def append(self, entry):
        self._entries.insert(-1, entry)


    def __len__(self):
        return len(self._entries) - 2