"""Test GC operations.

This test module assumes it has access to a postgresql instance as configured in
data/test_glib_config.json. The user requires database CREATE & DELETE rights.
"""


import pytest
from os.path import join, dirname, basename, splitext
from logging import basicConfig, DEBUG, INFO
from json import load
from collections import Counter
from microbiome.config import set_config, get_config
from microbiome.genetics.gene_pool import _gene_pool
from microbiome.genetics.gc_operations import gc_insert
from hashlib import md5
from pprint import pformat


# Load the test files.
with open(join(dirname(__file__), "data/test_gc_op_config.json"), "r") as file_ptr:
    test_config = load(file_ptr)


basicConfig(
    format='[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)


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
def test_basic_insert_456(gene_pool):
    """Test scenarios #4, #5 & #6 of GC insertion.

    Two codons with compatible input and output types are stacked.
    The compatible types mean a steady state exception is avoided
    (hence it is a 'basic' insert). Connectivity within the constraints
    of types and insertion location is random and so several variants
    may be created and one of which is correct."""
    addi_signature = "b7defebb20a51cfe22a012e880e2048e526daba406ae90c2a59a07d79c856d74"
    subi_signature = "b36d9bf9dfa7eac96dd70374ac949f64e6f72bce8bca30da7658ff0bdf2670b8"

    tgc = gene_pool[addi_signature]
    igc = gene_pool[subi_signature]
    graphs = {}
    counts = []
    for _ in range(10000):
        graph = gc_insert(tgc, igc, 'A')[0]['graph']
        code = md5(bytearray(pformat(graph), encoding='ascii')).hexdigest()
        counts.append(code)
        if not code in graphs: graphs[code] = graph
    print(pformat(dict(Counter(counts))))
    print(len(dict(Counter(counts))))
    print(pformat(graphs))