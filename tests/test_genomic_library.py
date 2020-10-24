"""Test the genomic library.

This test module assumes it has access to a postgresql instance as configured in
data/test_config.json. The user requires database CREATE & DELETE rights.
"""


import pytest
from os.path import join, dirname, basename, splitext
from logging import basicConfig, DEBUG
from json import load
from copy import deepcopy
from microbiome.config import set_config, get_config
from microbiome.genetics.genomic_library import genomic_library


# Load the test files.
with open(join(dirname(__file__), "data/test_glib_config.json"), "r") as file_ptr:
    test_config = load(file_ptr)


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


@pytest.mark.good
def test_len(glib):
    """Test construction & initialisation."""
    table = get_config()['tables']['test_genomic_library']
    cea_path = join(table['data_file_folder'], table['data_files'][0])
    with open(cea_path, "r") as cea_file:
        num_cea = len(load(cea_file))
    assert len(glib) == num_cea