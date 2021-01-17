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
from microbiome.genetics.genomic_library_entry_validator import NULL_GC


# Load the test files.
with open(join(dirname(__file__), "data/test_glib_config.json"), "r") as file_ptr:
    test_config = load(file_ptr)


NON_EXISTANT_SHA256 = "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd"
ANOTHER_NON_EXISTANT_SHA256 = "0123456789012345678901234567890123456789012345678901234567890123"
KNOWN_GOOD_SIGNATURE = "05fc73ef0115c380f1fa95648be1fe1bd7b23e8867bfb67c745ee6120ae2d499"
KNOWN_GOOD_SIGNATURE_NAME = "Random gc_graph_key choice."


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
    #gl._store._delete_db()


@pytest.mark.good
def test_initialise(glib):
    """Test construction & initialisation."""
    assert glib.isconnected()


@pytest.mark.good
def test_len(glib):
    """Test construction & initialisation.
    
    Count the number of entries in the datafiles list from the config
    and make sure that is how many entries were loaded into the genomic library.
    """
    table = get_config()['tables']['test_genomic_library']
    num_cea = 0
    for data_file in table['data_files']:
        cea_path = join(table['data_file_folder'], data_file)
        with open(cea_path, "r") as cea_file:
            num_cea += len(load(cea_file))
    assert len(glib) == num_cea


@pytest.mark.good
def test_getitem_found(glib):
    """Test __getitem__().
    
    Load the negate GC codon by its hash and check the name is correct. 
    """
    gc = glib[KNOWN_GOOD_SIGNATURE]
    assert gc['meta_data']['name'] == KNOWN_GOOD_SIGNATURE_NAME


@pytest.mark.good
def test_getitem_not_found(glib):
    """Test __getitem__().
    
    Try and load a non-existant GC. 
    """
    gc = glib[NON_EXISTANT_SHA256]
    assert gc is None


@pytest.mark.good
def test_check_references_good(glib):
    """Test _check_references().
    
    Make sure all the signatures from the first datafiles can be found.
    """
    table = get_config()['tables']['test_genomic_library']
    gcs = []
    for data_file in table['data_files']:
        cea_path = join(table['data_file_folder'], data_file)
        with open(cea_path, "r") as cea_file:
            for gc in load(cea_file):
                gcs.append(gc['signature'])
    assert not glib._check_references(gcs)


@pytest.mark.good
def test_check_references_bad(glib):
    """Test _check_references().
    
    Mix some non-existant signatures in with some valid ones.
    """
    table = get_config()['tables']['test_genomic_library']
    gcs = []
    for data_file in table['data_files']:
        cea_path = join(table['data_file_folder'], data_file)
        with open(cea_path, "r") as cea_file:
            for gc in load(cea_file):
                gcs.append(gc['signature'])
    gcs.append(NON_EXISTANT_SHA256)
    gcs.insert(int(len(gcs) / 2), ANOTHER_NON_EXISTANT_SHA256)
    naughty_list = glib._check_references(gcs)
    assert len(naughty_list) == 2
    assert NON_EXISTANT_SHA256 in naughty_list and ANOTHER_NON_EXISTANT_SHA256 in naughty_list


@pytest.mark.good
def test_load(glib):
    """Load some genetic codes from the library using a query."""
    assert glib.load([{'raw_num_codons': {'max': 1}}])


@pytest.mark.good
def test_load_bad_query(glib):
    """Load some genetic codes from the library using a query."""
    assert not glib.load([{'does_not_exist': {'max': 1}}])


@pytest.mark.good
def test_store(glib):
    """Store a set of tets codons."""
    with open(join(dirname(__file__), "data/test_codons.json"), "r") as file_ptr:
        test_codons = load(file_ptr)
    glib.store(test_codons)


@pytest.mark.good
def test_update(glib):
    """Update an entry in the genomic library."""
    glib.update([{'gca': NON_EXISTANT_SHA256}], [{'signature': KNOWN_GOOD_SIGNATURE}])
    assert len(glib.load([{'gca': NON_EXISTANT_SHA256}])) == 1
    glib.update([{'gca': NULL_GC}], [{'signature': KNOWN_GOOD_SIGNATURE}])
