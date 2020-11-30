"""A functional example that skips most of the tracking & logging.

This test focuses on the core logic of Erasmus without the complications of logging, work etc.
It makes no assumptions about the genomic library. 
"""


import pytest
from os.path import join, dirname, basename, splitext
from logging import basicConfig, DEBUG
from json import load
from copy import deepcopy
from microbiome.config import set_config, get_config
from microbiome.genetics.genomic_library import genomic_library
from microbiome.genetics.genomic_library_entry_validator import NULL_GC


# Load the test files.
with open(join(dirname(__file__), "data/test_example_config.json"), "r") as file_ptr:
    test_config = load(file_ptr)

    