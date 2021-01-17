"""Test a gene pool.

This test module assumes it has access to a postgresql instance as configured in
data/test_glib_config.json. The user requires database CREATE & DELETE rights.
"""


import pytest
from os.path import join, dirname, basename, splitext
from logging import basicConfig, DEBUG, INFO
from json import load
from microbiome.config import set_config, get_config
from microbiome.genetics.gene_pool import _gene_pool


# Load the test files.
with open(join(dirname(__file__), "data/test_glib_config.json"), "r") as file_ptr:
    test_config = load(file_ptr)


basicConfig(
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=INFO)


@pytest.fixture(scope="module")
def gene_pool():
    """Create a gene pool to be used in multiple test cases.

    The database and tables created are used in multiple tests. The last test
    will delete the database. data/test_glib_config.json is configured to delete
    any existing database of the same name prior to creation.
    """
    assert set_config(test_config)
    yield (gp := _gene_pool())


@pytest.mark.good
def test_initialise(gene_pool):
    """Test construction & initialisation."""
    assert len(gene_pool) > 0
