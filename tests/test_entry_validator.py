"""Validate database table structures."""


import pytest
from os.path import join, dirname, basename, splitext
from json import load
from microbiome.entry_column_meta_validator import entry_column_meta_validator
from logging import getLogger, basicConfig, DEBUG


basicConfig(
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)


@pytest.mark.good
@pytest.mark.parametrize("format_file", [
    join(dirname(__file__), "../microbiome/formats/genomic_library_entry_format.json"),
    join(dirname(__file__), "data/test_entry_format.json")
])
def test_format_files(format_file):
    """Load each definition and va;idate it."""
    with open(format_file, "r") as fileptr:
        for k, v in load(fileptr).items():
            assert 'meta' in v, "No 'meta' key in {} field {}.".format(format_file, k)
            assert entry_column_meta_validator(v['meta']), format_file + ":" + str(entry_column_meta_validator.errors)