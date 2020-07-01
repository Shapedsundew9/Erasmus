'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_work.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Monday, June 15th 2020, 6:54:13 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''

from logging import getLogger, basicConfig, DEBUG
basicConfig(filename='erasmus.log', level=DEBUG)

import pytest
from os.path import join, dirname
from json import load
from microbiome.genetics.genomic_library_entry_validator import genomic_library_entry_validator, NULL_GC
from microbiome.config import set_config, get_config

set_config(load(open(join(dirname(__file__), "test_config.json"), "r")))

from microbiome.creator import register_creator
from microbiome.work import register_work
from microbiome.worker import worker


gc_validator = genomic_library_entry_validator(load(open('./microbiome/formats/genomic_library_entry_format.json', "r")))


def test_work():
    work = {
        'name': 'Meta Evolution',
        'description': 'Evolving the evolver',
        'population_limit': 1000,
        'gene_pool': 'microbiome/genetics/mutations.py',
        'initial_query': [
            {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'unary_mutation': True}},
            {'gca': NULL_GC, 'gcb': NULL_GC, 'properties': {'binary_mutation': True}}
        ]
    }
    worker_config = {
        'work': register_work(work),
        'creator': register_creator({}),
    }
    w1 = worker(worker_config, lambda x: float(gc_validator(x)))
    w1.evolve()



    
