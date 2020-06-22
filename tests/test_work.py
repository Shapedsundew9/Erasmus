'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_work.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Monday, June 15th 2020, 6:54:13 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''

import pytest
from os.path import join, dirname
from json import load
from microbiome.config import set_config, get_config
from microbiome.work_registry_validator import work_registry_validator
from microbiome.creator import register_creator
from logging import getLogger, basicConfig, DEBUG
from sklearn.datasets import load_iris


basicConfig(filename='erasmus.log', level=DEBUG)


def test_work(self):
    worker_config = {
        'work': {
            'name': 'iris',
            'description': 'The sklearn "iris" dataset. https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html#sklearn.datasets.load_iris',
            'population_limit': 1000
        },
        'creator': register_creator({}),
        'fitness_function_file': 'ff_iris.py'
    }
    return worker_config




    
