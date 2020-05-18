'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_entry_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Sunday, March 29th 2020, 2:03:22 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


import pytest
from os.path import dirname, join
from json import load
from microbiome.entry_column_meta_validator import entry_column_meta_validator
from logging import getLogger, basicConfig, DEBUG


basicConfig(filename='erasmus.log', level=DEBUG)


@pytest.mark.parametrize("format_file", [
    "./microbiome/formats/genomic_library_entry_format.json",
    join(dirname(__file__), "test_entry_format.json")
])
def test_format_files(format_file):
    for k, v in load(open(format_file, "r")).items():
        assert 'meta' in v, "No 'meta' key in {} field {}.".format(format_file, k)
        assert entry_column_meta_validator(v['meta']), format_file + ":" + str(entry_column_meta_validator.errors)