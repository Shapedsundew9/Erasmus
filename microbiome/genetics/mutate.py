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


__MUTATIONS_FILE = 'mutations.py'
__MUTATION_PRIMITIVES_QUERY = [
    {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'unary_mutation': True}},
    {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'binary_mutation': True}}
]

__gp = gene_pool(__MUTATION_PRIMITIVES_QUERY, file_ptr=__MUTATIONS_FILE)


def refresh_mutations():
    # I know - private function
    __gp.__update()
    __gp.__header = "mutations = (\n"
    for gp in __gp.__gene_pool.values(): __gp.__header += "\t({}, {}),\n".format(gp['signature'], gp['properties']['binary_mutation'])
    __gp.__header += ")"
    __gp.__update() 

