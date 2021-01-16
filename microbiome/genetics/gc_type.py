"""Manages genetic code type interactions.

Genetic code types are identified by a 32-bit value.
See documentation for details.
"""


from json import load
from os.path import join, dirname


# Guranteed to be invalid
INVALID_NAME = {'name': 'invalid'}
INVALID_ANCESTORS = {'ancestors': []}
INVALID_VALUE = 262143


# Load type data
# TODO: Could convert numerical dict to a list if they are contiguous and start at 0.
with open(join(dirname(__file__), "../data/gc_types.json"), "r") as file_ptr:
    gc_type_lookup = load(file_ptr)
    gc_type_lookup['v2n'] = {int(k): v for k, v in gc_type_lookup['v2n'].items()}
    gc_type_lookup['n2v'] = {k: int(v) for k, v in gc_type_lookup['n2v'].items()}


def validate(gc_type_int):
    """Validate a gc_type_int.

    Args
    ----
    gc_type_int (int): The GC type value to validate.

    Returns
    -------
    (bool) True if the type is defined else false.
    """
    return gc_type_int in gc_type_lookup['v2n']


def asint(gc_type_str):
    """Convert a gc_type_str to its value representation.

    Args
    ----
    gc_type_str (str): The GC type name to convert to a value.

    Returns
    -------
    (int) GC type value.
    """
    return gc_type_lookup['n2v'].get(gc_type_str, INVALID_VALUE)


def asstr(gc_type_int):
    """Convert a gc_type_int to its string representation (name).

    Args
    ----
    gc_type_int (int): The GC type name to convert to a string.

    Returns
    -------
    (str) GC type name.
    """
    return gc_type_lookup['v2n'].get(gc_type_int, INVALID_NAME)['name']


def compatible(src_gc_type, dst_gc_type):
    """Validate src_gc_type is a decendent as dst_gc_type.

    Args
    ----
    src_gc_type (int): Value of the source gc_type.
    dst_gc_type (int): Value of the destination gc_type.

    Returns
    -------
    (bool) True if src_gc_type is a decendent of dst_gc_type.
    """
    if src_gc_type == dst_gc_type: return True
    return dst_gc_type in gc_type_lookup['v2n'].get(src_gc_type, INVALID_ANCESTORS)['ancestors']

