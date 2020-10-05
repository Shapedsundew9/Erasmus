'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/mutate.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, June 21st 2020, 7:03:04 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''

from inspect import getmembers, isfunction

from random import choice
from .gene_pool import gene_pool
from sys import path
from os.path import dirname, abspath, basename, isfile
from .genomic_library_entry_validator import NULL_GC


_MUTATIONS_FILE = 'mutations.py'
_MUTATION_PRIMITIVES_QUERY = [
    {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'unary_mutation': True}},
    {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'binary_mutation': True}}
]

_gp = gene_pool(_MUTATION_PRIMITIVES_QUERY, file_ptr=_MUTATIONS_FILE)


def refresh_mutations():
    # I know - private function
    _gp._update()
    _gp._header = "mutations = (\n"
    for gp in _gp._gene_pool.values(): _gp._header += "\t({}, {}),\n".format(gp['signature'], gp['properties']['binary_mutation'])
    _gp._header += ")"
    _gp._update() 

