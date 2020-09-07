"""
GCTD validator class definition.

Created Date: Monday, August 3rd 2020, 4:12:48 pm
Author: Shapedsundew9
"""


from cerberus import Validator
from json import load
from os.path import dirname, join
from logging import getLogger
from .gc_type_validator import gc_type_validator
from .gc_type import is_GC


class gc_graph_validator(Validator):
    """Validation of GCTD dictionary."""

    # TODO: Make errors ValidationError types for full disclosure
    # https://docs.python-cerberus.org/en/stable/customize.html#validator-error

    __logger = getLogger(__name__)
    __type_validator = gc_type_validator(load(open(join(dirname(__file__), "../formats/gc_type_format.json"), "r")))
 

    def _check_with_valid_type(self, field, value):
        if not gc_graph_validator.__type_validator(value): self._error(field, str(gc_graph_validator.__errors))


    def _check_with_valid_constant_type(self, field, value):
        if is_GC(value): self._error(field, "Constants cannot be a Genetic Code type.")
        self._check_with_valid_type(field, value)


    def _check_with_valid_index(self, field, value):
        pass


