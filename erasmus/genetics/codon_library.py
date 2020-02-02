'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 11:20:34 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''

from numpy import sqrt, reciprocal, isclose, array
from .codon import codon


def _store(x, y, z):
    x[y] = z


# There must be an 'input' and 'output' codon at positions 0 & 1 respectively.
codon_library = [
    # Input & output
    codon(lambda x: x, 'input'),
    codon(None, 'output'),

    # Constant definition
    codon(None, 'constant'),

    # Basic arithmetic
    codon(lambda x, y: x + y, 'add'),
    codon(lambda x, y: x - y, 'subtract'),
    codon(lambda x, y: x * y, 'multipy'),
    codon(lambda x, y: x / y, 'divide'),

    # Unary arithmetic
    codon(lambda x: sqrt(x), 'square root'),
    codon(lambda x: reciprocal(x), 'reciprical'),
    codon(lambda x: -x, 'negate'),

    # Basic conditional
    codon(lambda x, y: x < y, 'less than'),
    codon(lambda x, y: isclose(x, y), 'is close too'),

    # Basic logical
    codon(lambda x, y: x and y, 'and'),
    codon(lambda x, y: x or y, 'or'),

    # Unary logical
    codon(lambda x: not x, 'not'),

    # Branch
    codon(lambda x, y1, y2: y1 if x else y2, 'if then else'),

    # Addressing
    codon(lambda x, y: x[y], 'read', isMemory=True),
    codon(_store, 'write', isMemory=True)
]
