"""Tests for config.py."""


from os.path import join, dirname, basename, splitext
from logging import basicConfig, DEBUG
from json import load
from microbiome.config import update_config, get_config, set_config
from microbiome.config import get_errors, reset_config, save_config


_E02001_FORMAT_FILE = 'test_config_E02001_format.json'
_E02002_FORMAT_FILE = 'test_config_E02002_format.json'
_TEST_CONFIG_FILE = join(dirname(__file__), 'data', 'test_config.json')


basicConfig(
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)


def test_get_config():
    """Simple initialisation test."""
    get_config()


def test_set_config():
    """Set a new config."""
    with open(_TEST_CONFIG_FILE, 'r') as file_ptr:
        new_config = load(file_ptr)
    reset_config()
    set_config(new_config)


def test_save_config():
    """Save a config."""
    save_config()


def test_E02000(): #pylint: disable=C0103
    """Generate E02000.

    Mutate a table database name so that there is no definition for it.
    """
    assert not update_config({'tables': {'genomic_library': {'database': 'does_not_exist'}}})
    assert 'E02000' in get_errors()['tables'][0]['genomic_library'][0]['database'][0]


def test_E02001(): #pylint: disable=C0103
    """Generate E02001.

    Load the default global configuration, replace a default table with a broken
    table definition and validate.
    """
    broken_table_format = {'tables': {'genomic_library': {
        'format_file_folder': join(dirname(__file__), 'data'),
        'format_file': _E02001_FORMAT_FILE
    }}}
    reset_config()
    assert not update_config(broken_table_format)
    assert 'E02001' in get_errors()['tables'][0]['genomic_library'][0]['format_file'][0]


def test_E02002(): #pylint: disable=C0103
    """Generate E02002.

    Load the default global configuration, replace a default table with a broken
    table definition and validate.
    """
    broken_table_format = {'tables': {'genomic_library': {
        'format_file_folder': join(dirname(__file__), 'data'),
        'format_file': _E02002_FORMAT_FILE
    }}}
    reset_config()
    assert not update_config(broken_table_format)
    assert 'E02002' in get_errors()['tables'][0]['genomic_library'][0]['format_file'][0]
