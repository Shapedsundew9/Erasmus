'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from hashlib import md5 as hash_function
from zlib import compress, decompress
from pickle import dumps, loads
from base64 import b64encode, b64decode
from numpy import array
from numpy.random import randint
from inspect import signature
from .genetic_code_entry import genetic_code_entry as entry
from .genomic_library_entry import genomic_library_entry
from .codon_library import codon_library


# The genetic code is a list of gene/codon references & the connectivity
# entry = [inputs, reference to gene/codon, outputs]
# entries = [ input_entry, entry0, entry1, entry2, ... entryN, output_entry]
class genetic_code():


    def __init__(self, name=None, ancestor=None, codon_idx=None):
        # TODO: Optimisation idea: entries is a list of lists which is very inefficient.
        # Much less RAM can be used by arranging the components into numpy arrays
        # at the cost of construction time CPU.

        # self.entries = [input_entry, output_entry]
        self.entries = [entry(), entry()]
        self.name = name
        self.ancestor = ancestor
        if not codon_idx is None: self._initialise_with_codon(*codon_idx)


    def __getitem__(self, key):
        return self.entries[key]


    def __len__(self):
        return len(self.entries) - 2


    def _initialise_with_codon(self, c, i):
        self.name = c.name
        if not callable(c.func):
            self._initialise_with_constant(i)
        else:
            num_param = len(signature(c.func).parameters)
            if num_param == 2: self._initialise_with_binary(i)
            if num_param == 1: self._initialise_with_unary(i)
            if num_param == 3: self._initialise_with_ternary(i)


    def _initialise_with_constant(self, i):
        pass


    def _initialise_with_unary(self, i):
        self.append(entry([[0, 0]], True, i, [0]))


    def _initialise_with_binary(self, i):
        self.append(entry([[0, 0], [0, 1]], True, i, [0]))


    def _initialise_with_ternary(self, i):
        self.append(entry([[0, 0], [0, 1], [0, 2]], True, i, [0]))


    def id(self):
        return hash_function(dumps(self.entries)).hexdigest()


    def zserialise(self):
        return b64encode(compress(dumps(self.entries), 9))


    def zdeserialise(self, obj):
        self.entries = loads(decompress(b64decode(obj)))


    def append(self, entry):
        self.ancestor = self.id()
        self.entries.insert(-1, entry)


    def insert(self, pos, entry):
        self.ancestor = self.id()
        self.entries.insert(pos + 1, entry)


    def make_library_entry(self, meta_data=None):
        return genomic_library_entry(self.zserialise(), self.id(), self.ancestor, self.name, meta_data)


    def random_index(self):
        return randint(len(self))

    
