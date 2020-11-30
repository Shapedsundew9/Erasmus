"""Manages genetic code type interactions.

Genetic code types are identified by a 32-bit value.
See documentation for details.
"""


from json import load
from os.path import join, dirname


# Guranteed to be invalid
INVALID_NAME = 'invalid'
INVALID_VALUE = 262143


# Load type data
with open(join(dirname(__file__), "../data/gc_types.json"), "r") as file_ptr:
    gc_type_lookup = load(file_ptr)
    gc_type_lookup['value'] = {int(v): n for v, n in gc_type_lookup['value'].items()}
    gc_type_lookup['group'] = {k: set(v) for k, v in gc_type_lookup['group'].items()}
with open(join(dirname(__file__), "../data/gc_group_types.json"), "r") as file_ptr:
    temp = load(file_ptr)
    gc_group_types = {group: {'types': set(value['types']), 'sub-groups': set(value['sub-groups'])} for group, value in temp.items()}
with open(join(dirname(__file__), "../data/gc_translation_types.json"), "r") as file_ptr:
    gc_translation_types = load(file_ptr)


def validate(gc_type):
    """Validate a gc_type.

    Args
    ----
    gc_type (str/int): The gc_type name or value to validate.

    Returns
    -------
    (bool) True if the type is defined else false.
    """
    return gc_type in gc_type_lookup['name'] or gc_type in gc_type_lookup['value']


def asint(gc_type):
    """Convert a gc_type to its value representation.

    Args
    ----
    gc_type (str): The gc_type name to convert to a value.

    Returns
    -------
    (int) gc_type value.
    """
    return gc_type_lookup['name'].get(gc_type, INVALID_VALUE)


def asstr(gc_type):
    """Convert a gc_type to its string representation (name).

    Args
    ----
    gc_type (int): The gc_type name to convert to a string.

    Returns
    -------
    (str) gc_type name.
    """
    return gc_type_lookup['value'].get(gc_type, INVALID_NAME)


def compatible(src_gc_type, dst_gc_type):
    """Validate src_gc_type is a subset or the same set as dst_gc_type.

    Args
    ----
    src_gc_type (str): Name of the source gc_type.
    dst_gc_type (str): Name of the destination gc_type.

    Returns
    -------
    (bool) True if str_gc_type represents a subset or the same set as dst_gc_type.
    """
    if dst_gc_type == 'any': return True
    if src_gc_type == 'any': return False

    if src_gc_type in gc_group_types:
        src_type_set = gc_group_types[src_gc_type]['types']
    elif src_gc_type in gc_translation_types:
        src_type_set = gc_group_types[gc_translation_types[src_gc_type]['group']]['types']
    else:
        src_type_set = {src_gc_type}

    if dst_gc_type in gc_group_types and src_gc_type != 'any':
        dst_type_set = gc_group_types[dst_gc_type]['types']
    elif dst_gc_type in gc_translation_types:
        dst_type_set = gc_group_types[gc_translation_types[dst_gc_type]['group']]['types']
    else:
        dst_type_set = {dst_gc_type}

    return set(src_type_set) <= set(dst_type_set)


def member_of(gc_type):
    """Return the set of gc_type groups gc_type is a member of.

    Args
    ----
    gc_type (str): The gc_type name.

    Returns
    -------
    (set(str)) The set of gc_type groups gc_type is a member of. 
    """
    return gc_type_lookup['group'].get(gc_type, set())