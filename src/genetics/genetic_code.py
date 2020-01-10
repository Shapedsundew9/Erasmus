'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from hashlib import sha512
from zlib import compress, decompress
from pickle import dumps, loads
from base64 import b64encode, b64decode
from numpy.random import randint
from .genetic_code_entry import genetic_code_entry as entry


# The genetic code is a list of gene/codon references & the connectivity
# entry = [inputs, reference to gene/codon, outputs]
# _entries = [ input_entry, entry0, entry1, entry2, ... entryN, output_entry]
class genetic_code():

    def __init__(self, name='Empty', codon_idx=None, ancestor=None):
        # TODO: Optimisation idea: _entries is a list of lists which is very inefficient.
        # Much less RAM can be used by arranging the components into numpy arrays
        # at the cost of construction time CPU.

        # self._entries = [input_entry, output_entry]
        self._entries = [entry(), entry()]
        self.name = name
        self.ancestor = ancestor
        if not codon_idx is None: self._initialise_with_codon(*codon_idx)


    def __getitem__(self, key):
        return self._entries[key]


    def __len__(self):
        return len(self._entries) - 2


    def id(self):
        return sha512(dumps(self._entries)).hexdigest()


    def zserialise(self):
        return b64encode(compress(dumps(self._entries), 9))


    def zdeserialise(self, obj):
        self._entries = loads(decompress(b64decode(obj)))


    def append(self, entry):
        self.ancestor = self.id()
        self._entries.insert(-1, entry)

    def insert(self, pos, entry):
        self.ancestor = self.id()
        self._entries.insert(pos + 1, entry)


    def random_index(self):
        return randint(len(self))


    def _initialise_with_codon(self, c, i):
        self.name = c.name
        if c.isConstant: self._initialise_with_constant(i)
        if c.isUnary: self._initialise_with_unary(i)
        if c.isBinary: self._initialise_with_binary(i)
        if c.isTernary: self._initialise_with_ternary(i)


    def _initialise_with_constant(self, i):
        pass


    def _initialise_with_unary(self, i):
        self.append(entry([[0, 0]], True, i, [0]))


    def _initialise_with_binary(self, i):
        self.append(entry([[0, 0], [0, 1]], True, i, [0]))


    def _initialise_with_ternary(self, i):
        self.append(entry([[0, 0], [0, 1], [0, 2]], True, i, [0]))


    
