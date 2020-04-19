'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_entry_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Sunday, March 29th 2020, 2:03:22 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from os.path import isfile
from json import load
from microbiome.genetics.entry_validator import entry_validator, ENTRY_VALIDATION_SCHEMA


CODON_LIBRARY_FILE = "./microbiome/genetics/codon_library.json"


# Validate the codon library
def test_codon_library():
    if not isfile(CODON_LIBRARY_FILE): assert False, "Cannot find {}".format(CODON_LIBRARY_FILE)
    with open(CODON_LIBRARY_FILE, "r") as file_ptr: codon_library = load(file_ptr)
    validator = entry_validator(ENTRY_VALIDATION_SCHEMA)
    for codon in codon_library: assert validator(codon), codon["meta_data"]["name"] + ":" + str(validator.errors)
    for codon in codon_library: validator.normalized(codon)


# TODO: Add some non-codon test cases
# TODO: Add some negative tests