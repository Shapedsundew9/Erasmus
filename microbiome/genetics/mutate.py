'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/mutate.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, June 21st 2020, 7:03:04 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''

from inspect import getmembers, isfunction
from importlib import import_module, reload
from random import choice
from .gene_pool import gene_pool
from sys import path
from os.path import dirname, abspath, basename, isfile
from .genomic_library_entry_validator import NULL_GC


__MUTATIONS_FILE = "mutations.py"
__MUTATION_PRIMITIVES_QUERY = [
    {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'unary_mutation': True}},
    {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'binary_mutation': True}}
]

if not isfile(__MUTATIONS_FILE): gene_pool(__MUTATION_PRIMITIVES_QUERY, file_ptr=__MUTATIONS_FILE)
path.insert(1, dirname(abspath(__MUTATIONS_FILE)))
__mutations_module = import_module(__MUTATIONS_FILE[:-3])
__all_functions = None


# This assumes all function either take a single GC Entry or 2 GC Entries.
# TODO: This should probably take a GC instance (or 2)
def mutate(gca, population):
    func = choice(__all_functions)
    return func[1](gca, choice(population)) if len(func[1].__defaults__) == 2 else func[1](gca)    


def refresh_mutations():
    global __all_functions
    # OPTIMISATION: Could check to see if the source code has changed before reloading
    reload(__mutations_module)
    __all_functions = getmembers(__mutations_module, isfunction)
