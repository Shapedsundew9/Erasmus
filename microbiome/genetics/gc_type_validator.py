"""
GCTD validator class definition.

Created Date: Monday, August 3rd 2020, 4:12:48 pm
Author: Shapedsundew9
"""


from cerberus import Validator
from json import load
from os.path import dirname, join
from logging import getLogger


class gc_type_validator(Validator):
    """Validation of GCTD dictionary."""

    # TODO: Make errors ValidationError types for full disclosure
    # https://docs.python-cerberus.org/en/stable/customize.html#validator-error

    __logger = getLogger(__name__)
    __object_validator = Validator(
        load(open(join(dirname(__file__), "gc_type_object_param_format.json"), "r")))
    __numeric_validator = Validator(
        load(open(join(dirname(__file__), "gc_type_numeric_param_format.json"), "r")))

    def _check_with_valid_base_type(self, field, value):
        if value['object'] and (value['integer'] or value['floating_point']):
            self._error(
                field, "A type cannot be both and object and a numeric.")

    def _check_with_valid_parameters(self, field, value):
        if self.document['base_type']['object']:
            if not gc_type_validator.__object_validator(value):
                self._error(field, gc_type_validator.__object_validator.errors)
            if value['obj_id'] < 128:
                gc_type_validator.__logger.debug(
                    "GCTD of RESERVED object type validated.")
            if value['obj_id'] > 895:
                gc_type_validator.__logger.info(
                    "GCTD of user defined object type validated.")
        else:
            if not gc_type_validator.__numeric_validator(value):
                self._error(
                    field, gc_type_validator.__numeric_validator.errors)
            if self.document['base_type']['floating_point'] and not value['sign']:
                self._error(field, "Floating point types must have sign == 1.")
