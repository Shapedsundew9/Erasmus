'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Saturday, April 11th 2020, 2:51:52 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

import pytest
from os.path import join, dirname
from json import load, dump, dumps
from microbiome.config import set_config
from microbiome.genetics.genomic_library import genomic_library
from logging import getLogger, basicConfig, DEBUG


basicConfig(filename='erasmus.log', level=DEBUG)


def test_genomic_library():
    set_config(load(open(join(dirname(__file__), "test_config.json"), "r")))
    reference = load(open(join(dirname(__file__), "test_codon_library.json"), "r"))
    for r in reference: r['created'] = None
    gl = genomic_library("test_genomic_library", "test_database")
    result = gl.load([])
    for r in result: r['created'] = None
    # with open("test_codon_library.json", "w") as file_ptr: dump(gl.load([]), file_ptr, indent=4, sort_keys=True)
    assert dumps(result, indent=4, sort_keys=True) == dumps(reference, indent=4,sort_keys=True)
