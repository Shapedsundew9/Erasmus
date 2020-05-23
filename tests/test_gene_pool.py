'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_gene_pool.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Thursday, January 30th 2020, 7:26:37 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

import pytest
from os.path import join, dirname
from json import load
from microbiome.config import set_config
from microbiome.genetics.gene_pool import gene_pool
from logging import getLogger, basicConfig, DEBUG


basicConfig(filename='erasmus.log', level=DEBUG)


def test_gene_pool():
    set_config(load(open(join(dirname(__file__), "test_config.json"), "r")))
    gene_pool('007')