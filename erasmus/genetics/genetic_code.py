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
from random import choices
from inspect import signature
from copy import copy
from .genetic_code_entry import genetic_code_entry as entry
from .genetic_code_entry import ref, inputs, outputs
from .codon_library import codon_library


_INPUT_ENTRY = 0
_OUTPUT_ENTRY = -1


# The genetic code is a list of gene/codon references & the connectivity
# entry = [inputs, reference to gene/codon, outputs]
# entries = [entry0, entry1, entry2, ... entryN]
class genetic_code():


    def __init__(self, name=None, ancestor=None, codon_idx=None, constant=None, idx=None, library_entry=None):
        # TODO: Optimisation idea: entries is a list of entry's which is very inefficient.
        # Much less RAM can be used by arranging the components into numpy arrays
        # at the cost of construction time CPU.

        if library_entry == None:
            self.name = name
            self.ancestor = ancestor
            self.idx = idx
            if not codon_idx is None:
                self.entries = []
                self._initialise_with_codon(*codon_idx, constant)
            else:
                # self.entries = [input_entry, output_entry]
                self.entries = [entry(idx=0), entry(idx=1)]
        else:
            self.zdeserialise(library_entry.data, library_entry.idx)
            self.name = library_entry.name
            self.ancestor = library_entry.ancestor
            self.idx = library_entry.idx
 

    def __getitem__(self, key):
        return self.entries[key]


    def __len__(self):
        return len(self.entries)


    def __str__(self):
        ret_val = "Name: {0}, Ancestor: {1}, Library Index: {2}\n".format(self.name, self.ancestor, self.idx)
        for e in self.entries: ret_val += str(e) + "\n"
        return ret_val


    def _initialise_with_codon(self, c, i, constant):
        self.name = c.name
        if not callable(c.func):
            self.append(entry([], i, [constant]))
        else:
            self.append(entry([ref()] * len(signature(c.func).parameters), i, [0]))


    def clone(self):
        new_me = copy(self)
        new_me.ancestor = self.idx
        new_me.idx = None
        new_me.name = None
        return new_me


    def num_inputs(self):
        return len(self.entries[0].input)


    def num_outputs(self):
        return len(self.entries[-1].input)


    def id(self):
        return hash_function(dumps(self.entries)).hexdigest()


    # TODO: Move the derialisation to the entry and reduce the overall string size.
    def zserialise(self):
        return b64encode(compress(dumps(self.entries), 9))


    def zdeserialise(self, obj, idx):
        self.entries = loads(decompress(b64decode(obj)))
        self.idx = idx


    def append(self, code):
        self.entries.insert(-1, code)
        return self


    def extend_inputs(self, num):
        self.entries[0].input.extend([ref()] * num)

    
    def extend_outputs(self, num):
        self.entries[-1].input.extend([ref()] * num)


    def insert_entry(self, new_entry, pos):
        self.entries.insert(pos, new_entry)


    def make_entry(self):
        return entry(genetic_code=self)


    def random_index(self):
        return 0 if not len(self) else randint(len(self))

