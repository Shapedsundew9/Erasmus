"""Test the genomic library.

This test module assumes it has access to a postgresql instance as configured in
data/test_config.json. The user requires database CREATE & DELETE rights.
"""


import pytest
from os.path import join, dirname, basename, splitext
from logging import basicConfig, DEBUG
from json import load
from copy import deepcopy
from microbiome.config import set_config
from microbiome.genetics.genomic_library import genomic_library


# Load the test files.
with open(join(dirname(__file__), "data/test_config.json"), "r") as file_ptr:
    test_config = load(file_ptr)


# Update the format_folder_path to be where ever these tests run from.
folder = join(dirname(__file__), 'data')
for tbl in ('test_history_decimation', 'test_table', 'test_broken_table'):
    test_config['tables'][tbl]['format_file_folder'] = folder


basicConfig(
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)


@pytest.fixture(scope="module")
def glib():
    """Create a genomic library to be used in multiple test cases.

    The database and tables created are used in multiple tests. The last test
    will delete the database. data/test_config.json is configured to delete
    any existing database of the same name prior to creation.
    """
    assert set_config(test_config)
    yield (gl := genomic_library())
    gl._store._delete_db()


@pytest.mark.good
def test_initialise(glib):
    """Test construction & initialisation."""
    assert glib.isconnected()