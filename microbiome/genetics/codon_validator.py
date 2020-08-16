"""
GCTD validator class definition.

Created Date: Monday, August 3rd 2020, 4:12:48 pm
Author: Shapedsundew9
"""


from cerberus import Validator
from json import load
from os.path import dirname, join
from logging import getLogger


class codon_validator(Validator):
    """Validation of GCTD dictionary."""

    # TODO: Make errors ValidationError types for full disclosure
    # https://docs.python-cerberus.org/en/stable/customize.html#validator-error

    __logger = getLogger(__name__)
 


