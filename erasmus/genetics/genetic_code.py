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
from numpy import array, float32
from numpy.random import randint, uniform
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
                self.entries = [entry(idx=0, is_codon=True), entry(idx=1, is_codon=True)]
        else:
            self.zdeserialise(library_entry.data, library_entry.idx)
            self.name = library_entry.name
            self.ancestor = library_entry.ancestor
            self.idx = library_entry.idx

            # This is a default case if the constant codon library entry is chosen it must have a value.
            # Really these values should be managed by the mutations.
            if len(self.entries) == 1 and codon_library[self.idx].isConstant: self.entries[0].output = outputs([uniform()])


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
        if c.isConstant:
            self.append(entry([], i, True, [constant]))
        elif c.isIO:
            self.append(entry([], i, True, []))
        else:
            num_params = len(signature(c.func).parameters)
            if c.isMemory: num_params -= 1
            self.append(entry([ref() for _ in range(num_params)], i, True, [float32(0.0)]))


    def clone(self):
        new_me = copy(self)
        new_me.ancestor = self.idx
        new_me.idx = None
        new_me.name = None
        return new_me


    def num_inputs(self):
        return len(self.entries[_INPUT_ENTRY].input)


    def num_outputs(self):
        return len(self.entries[_OUTPUT_ENTRY].input)


    def id(self):
        return hash_function(dumps(self.entries)).hexdigest()


    # TODO: Move the serialisation to the entry and reduce the overall string size.
    def zserialise(self):
        # TODO: Strip out the output values for everything but constants to reduce size
        return b64encode(compress(dumps(self.entries), 9))


    def zdeserialise(self, obj, idx):
        self.entries = loads(decompress(b64decode(obj)))
        self.idx = idx


    def append(self, code):
        self.entries.insert(_OUTPUT_ENTRY, code)
        return self


    def extend_inputs(self, num):
        self.entries[_INPUT_ENTRY].input.extend([ref() for _ in range(num)])
        self.entries[_INPUT_ENTRY].output.extend([float32(0.0)] * num)

    
    def extend_outputs(self, num):
        self.entries[_OUTPUT_ENTRY].input.extend([ref() for _ in range(num)])
        self.entries[_OUTPUT_ENTRY].output.extend([float32(0.0)] * num)


    def insert_entry(self, new_entry, pos):
        self.entries.insert(pos, new_entry)


    def make_entry(self):
        return entry(genetic_code=self)


    def get_inputs(self, i):
        return array([self.entries[r.row].output[r.pos] for r in self.entries[i].input], dtype=float32)


    def random_index(self):
        row = randint(len(self))
        return row if row > 1 else 1 

'''
    def code_graph(self):
        self.graph = Graph()
        for i, g in enumerate(self.genetic_code.entries, 1):

'''