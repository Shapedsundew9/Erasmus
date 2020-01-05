'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 11:20:34 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''

import numpy as np
from codon import codon


codon_library = [
    # The output codon (has to be element 0)
    codon(lambda x: np.array(x).flatten(), 'output', isUnary=True),

    # Basic arithmetic
    codon(lambda x, y: x + y, 'add'),
    codon(lambda x, y: x - y, 'subtract'),
    codon(lambda x, y: x * y, 'multipy'),
    codon(lambda x, y: x / y, 'divide'),

    # Unary arithmetic
    codon(lambda x: np.sqrt(x), 'square root', isUnary=True),
    codon(lambda x: np.reciprical(x), 'reciprical', isUnary=True),
    codon(lambda x: -x, 'negate', isUnary=True),

    # Basic conditional
    codon(lambda x, y: x < y, 'less than'),
    codon(lambda x, y: np.isclose(x, y), 'is close too'),

    # Basic logical
    codon(lambda x, y: x and y, 'and'),
    codon(lambda x, y: x or y, 'or'),

    # Unary logical
    codon(lambda x: not x, 'not', isUnary=True),

    # Branch
    codon(lambda x, y1, y2: y1 if x else y2, 'if then else', isTernary=True),

    # Addressing
    codon(lambda x, y: x[np.int(y)], 'index', isAddressing=True),
    codon(lambda x, y1, y2: x[np.int(y1):np.int(y2)], 'range index', isTernary=True, isAddressing=True),
    codon(lambda x, y: np.concatenate((x, y)), 'range index', isAddressing=True)
]