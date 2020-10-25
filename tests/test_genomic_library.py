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


NON_EXISTANT_SHA256 = "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd"


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
    
    Load the negate GC codon by its hash and chack the name is correct. 
    """
    gc = glib["1e3595731a3915c541b8b58eece28de636898e6d46193268570b39eb8ffb5e0c"]
    assert gc['meta_data']['name'] == 'negate'


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
    
    Vandalise a GCA reference 
    """
    gcs = glib.load([{'raw_num_codons': {'min': 2}}], ['signature'])
    assert not glib._check_references(gcs)