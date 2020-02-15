'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 11:20:34 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''

from numpy import sqrt, reciprocal, isclose, array, float32, uint32
from .codon import codon


def _store(x, y, z):
    return x.set(y, z)


# WARNING: Once a genomic library is created codons CANNOT BE REMOVED
# TODO: In theory they can be added but the code does not yet support this.
codon_library = [
    ############################################################
    # Special codons
    ############################################################

    # Input & output
    # There must be an 'input' and 'output' codon at positions 0 & 1 respectively.
    codon(None, 'input', isIO=True),
    codon(None, 'output', isIO=True),

    # Constant definition
    # Constants have special treatment for storing in the genomic library
    codon(None, 'constant', isConstant=True),

    ############################################################


    # These codons have no special treatment
    # Basic arithmetic
    codon(lambda x, y: x + y, 'add'),
    codon(lambda x, y: x - y, 'subtract'),
    codon(lambda x, y: x * y, 'multipy'),
    codon(lambda x, y: float32(0.0) if y == float32(0.0) else x / y, 'divide'),

    # Unary arithmetic
    codon(lambda x: float32(0.0) if x < 0 else sqrt(x), 'square root'),
    codon(lambda x: float32(0.0) if x == float32(0.0) else reciprocal(x), 'reciprical'),
    codon(lambda x: -x, 'negate'),

    # Basic conditional
    codon(lambda x, y: x < y, 'less than'),
    codon(lambda x, y: isclose(x, y), 'is close too'),

    # Basic logical
    codon(lambda x, y: bool(x) and bool(y), 'and'),
    codon(lambda x, y: bool(x) or bool(y), 'or'),

    # Unary logical
    codon(lambda x: not bool(x), 'not'),

    # Branch
    codon(lambda x, y1, y2: y1 if x else y2, 'if then else'),

    # Addressing
    codon(lambda x, y: x[uint32(y)], 'read', isMemory=True),
    codon(_store, 'write', isMemory=True)
]
