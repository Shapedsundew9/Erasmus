"""Test GC operations.

This test module assumes it has access to a postgresql instance as configured in
data/test_glib_config.json. The user requires database CREATE & DELETE rights.
"""


import pytest
from os.path import join, dirname, basename, splitext
from logging import basicConfig, DEBUG, INFO, getLogger
from json import load
from collections import Counter
from microbiome.config import set_config, get_config
from microbiome.genetics.gene_pool import _gene_pool
from microbiome.genetics.gc_operations import gc_insert
from hashlib import md5
from pprint import pformat
from statistics import stdev, mean
from random import randint


# Constants
ADDI_SIGNATURE = "b7defebb20a51cfe22a012e880e2048e526daba406ae90c2a59a07d79c856d74"
SUBI_SIGNATURE = "b36d9bf9dfa7eac96dd70374ac949f64e6f72bce8bca30da7658ff0bdf2670b8"


# Load the test files.
with open(join(dirname(__file__), "data/test_gc_op_config.json"), "r") as file_ptr:
    test_config = load(file_ptr)
# Load the results file.
with open(join(dirname(__file__), "data/test_gc_op_results.json"), "r") as file_ptr:
    results = load(file_ptr)


basicConfig(
    format='[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)


_logger = getLogger(__name__)


@pytest.fixture(scope="module")
def gene_pool():
    """Create a gene pool to be used in multiple test cases.

    The database and tables created are used in multiple tests. The last test
    will delete the database. data/test_glib_config.json is configured to delete
    any existing database of the same name prior to creation.
    """
    assert set_config(test_config)
    yield (gp := _gene_pool(file_ptr="test_gp.py"))


@pytest.mark.good
def test_basic_insert_2_simple(gene_pool):
    """Test case #2 of GC insertion.

    Two codons with compatible input and output types are stacked.
    The compatible types mean a steady state exception is avoided
    (hence it is a 'basic' insert). Connectivity within the constraints
    of types and insertion location is random and so several variants
    may be created and one of which is correct.
    """
    tgc, igc = gene_pool[ADDI_SIGNATURE], gene_pool[SUBI_SIGNATURE]
    graph = gc_insert(tgc, igc, 'A')[0]['graph']
    code = md5(bytearray(pformat(graph), encoding='ascii')).hexdigest()

    """
    # Debug code
    if not code in results['basic_insert_2'].keys():
        graphs = {}
        for _ in range(100):
            graph = gc_insert(tgc, igc, 'A')[0]['graph']
            code = md5(bytearray(pformat(graph), encoding='ascii')).hexdigest()
            graphs[code] = graph
        print(pformat(graphs))
    """
    assert code in results['basic_insert_2'].keys()


@pytest.mark.good
def test_basic_insert_2_stats(gene_pool):
    """Check the statistics of case #2 in the basic scenario.

    The connectivity of the inserted GC is uniform random. To verify
    randomness is just that this test checks that the standard deviation
    of the allowable variants is at least moderately likely. ;)

    NB: The maths on this may be shakey!!!

    In this scenario there are 4 possible results.
    Empirical analysis shows the standard deviation of the occurances of the 
    four results in 1000 runs of 1000 insertions is min:0.816, max:35.355,
    avg:14.370, stdev:5.927.

    3.5-sigma is 1 in 2149 = 35.115
    So if 1000 inserts have a stdev > 35.115 three times in a row that is
    about a 1 in 10 billion shot.    
    """
    tgc, igc = gene_pool[ADDI_SIGNATURE], gene_pool[SUBI_SIGNATURE]
    func = lambda x: [md5(bytearray(pformat(gc_insert(tgc, igc, 'A')[0]['graph']), encoding='ascii')).hexdigest() for _ in range(x)]
    unlikely = 0
    for iteration in range(3):
        if stdev(Counter(func(1000)).values()) > 35.115:
            unlikely += 1

    if unlikely == 1: _logger.info("Suspicious: Random connection probability > 1 in 2149")
    elif unlikely == 2: _logger.warn("Very suspicious: Random connection probability > 1 in 4618201")
    elif unlikely == 3: _logger.error("Something is wrong: Random connection probability > 1 in 9924513949")
    assert unlikely < 3


@pytest.mark.good
@pytest.mark.parametrize("a, b", tuple((randint(0, 100), randint(0, 100)) for _ in range(100)))
def test_basic_insert_2_identity(gene_pool, a, b):
    """Inserting a graph should not change the function of the original.

    Insertion is a null operation from a functionality perspective.
    Do the test 100 times for a strong statistical likelihood of
    generating all variants and not getting a 'unlucky' correct
    mathematical result.
    """
    tgc, igc = gene_pool[ADDI_SIGNATURE], gene_pool[SUBI_SIGNATURE]
    gcs = gc_insert(tgc, igc, 'A')
    rgc_signature = gcs[0]['signature']
    gene_pool.add(gcs)
    rgc = gene_pool[rgc_signature]
    assert tgc['_func']((a, b)) == rgc['_func']((a, b))


@pytest.mark.good
@pytest.mark.parametrize("a, b", tuple((randint(0, 100), randint(0, 100)) for _ in range(10)))
def test_basic_insert_3_identity(gene_pool, a, b):
    """Inserting a graph should not change the function of the original.

    Insertion is a null operation from a functionality perspective.
    Do the test 10 times to avoid getting an 'unlucky' correct
    mathematical result.
    """
    tgc, igc = gene_pool[ADDI_SIGNATURE], gene_pool[SUBI_SIGNATURE]
    gcs = gc_insert(tgc, igc, 'B')
    rgc_signature = gcs[0]['signature']
    gene_pool.add(gcs)
    rgc = gene_pool[rgc_signature]
    assert tgc['_func']((a, b)) == rgc['_func']((a, b))


@pytest.mark.good
@pytest.mark.parametrize("a, b", tuple((randint(0, 100), randint(0, 100)) for _ in range(10)))
def test_basic_insert_4_identity(gene_pool, a, b):
    """Inserting a graph should not change the function of the original.

    Insertion is a null operation from a functionality perspective.
    Do the test 10 times to avoid getting an 'unlucky' correct
    mathematical result.
    """
    _logger.debug("Pushing gene pool to genomic library.")
    gene_pool.push()
    _logger.debug("Querying for generation 1.")
    gen1 = gene_pool.gl([{"generation": 1, "limit": 1}])
    gene_pool.add(gen1)
    tgc = gene_pool[gen1[0]['signature']]
    igc = gene_pool[ADDI_SIGNATURE]
    _logger.debug("Case 4 insertion")
    gcs = gc_insert(tgc, igc, 'A')
    rgc_signature = gcs[0]['signature']
    gene_pool.add(gcs)
    rgc = gene_pool[rgc_signature]
    assert tgc['_func']((a, b)) == rgc['_func']((a, b))
