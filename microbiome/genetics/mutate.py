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


__mutations_module = import_module("mutations.py")
__all_functions = None


def mutate(gca, population):
    func = choice(__all_functions)
    return func[1](gca, choice(population)) if len(func[1].__defaults__) == 2 else func[1](gca)    


def refresh_mutations():
    global __all_functions
    # OPTIMISATION: Could check to see if the source code has changed before reloading
    reload(__mutations_module)
    __all_functions = getmembers(__mutations_module, isfunction)
