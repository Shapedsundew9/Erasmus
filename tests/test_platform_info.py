"""Test platform info collection."""

import pytest
from os.path import join, dirname, splitext, basename
from json import load
from microbiome.platform_info import get_platform_info
from logging import getLogger, basicConfig, DEBUG


basicConfig(
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)


@pytest.mark.good
def test_platform_info_init():
    """Basic validation."""
    assert get_platform_info()

