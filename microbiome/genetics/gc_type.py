"""Manages genetic code type interactions.

Genetic code types are identified by a 16-bit value.

Each type has an affinity to itself and all other types that is used to govern
the "physics" of genetic code assembly.

__affinity is a matrix of values 0.0 <= x <= 1.0 defining how attracted
types are to each other. 0.0 being not at all, 1.0 being very much. The
paradigm being physical interactions. Note that affinity is not symmetrical
if type X has a high affinity to type Y it does not follow that type Y necessarily
has a high affinity for type X. Typically it is the cost of conversion in information
or behavioural loss / change that drives the affinity value.

Examples (made up affinities):
    int8-int8 = 1.0: The best match for a type is (universaly?) itself.
    int8-int16 = 0.95: An int8 can very effectively be represented by an int16 at the cost of some overflow behaviour.
    int16-int8 = 0.2: There is a substantial chance of truncation going from 16 bits to 8.
    dict:float32 = 0.0: An implicit conversion from a dictionary type to a float does not make sense.
"""


from numpy import float32, array, uint16
from scipy.sparse import coo_matrix
from json import load
from os.path import dirname, join
from logging import getLogger
from bitstruct import pack_dict, unpack_dict
from pprint import pformat
from .gc_type_validator import gc_type_validator


__logger = getLogger(__name__)
__gc_type_validator = gc_type_validator(load(open(join(dirname(__file__), "gc_type_format.json"), "r")))
__BIT_FIELDS = {'fmt': 'u1u3u12', 'names': ('RESERVED', 'base_type', 'parameters')}
__BASE_TYPE = {'fmt': 'u1u1u1', 'names': ('object', 'integer', 'floating_point')}
__NUMERIC_PARAM = {'fmt': 'u1u3u3u1u1u2', 'names': ('sign', 'log_size', 'n_dim', 'exact', 'RESERVED', 't_idx')}
__OBJECT_PARAM = {'fmt': 'u10u2', 'names': ('obj_id', 't_idx')}


def gc_type_dict(gc_type):
    """Return a dictionary representation of a Genetic Code Type Definition.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        dict: A dictionary with keys and values defined by ref.  
    """
    definition = unpack_dict(**gc_type.__BIT_FIELDS, data=gc_type)
    retval = {'base_type': unpack_dict(**__BASE_TYPE, data=definition['base_type'])}
    param_def = __OBJECT_PARAM if retval['base_type']['object'] else __NUMERIC_PARAM
    retval['parameters'] = unpack_dict(**param_def, data=definition['parameters'])
    return retval


def is_int(gc_type):
    """Genetic Code Type Definition integer test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is integer. Returns False for all non-integer types
        including numeric.  
    """
    return gc_type & 0x2000 and not gc_type & 0x1000


def is_fp(gc_type):
    """Genetic Code Type Definition floating point test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is floating point. Returns False for all non-floating point types
        including numeric.  
    """
    return gc_type & 0x1000 and not gc_type & 0x2000


def is_numeric(gc_type):
    """Genetic Code Type Definition numeric test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is numeric. Returns False for all other types.  
    """
    return gc_type & 0x2000 and gc_type & 0x1000


def is_object(gc_type):
    """Genetic Code Type Definition object test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is object else False.  
    """
    return bool(gc_type & 0x4000)


def is_template(gc_type):
    """Genetic Code Type Definition template test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is templated else False.
    """
    return bool(gc_type & 0x3)


def __type_to_idx(gc_type):
    idx = (gc_type >> 2) | 0x400 if is_object(gc_type) else gc_type >> 4
    return idx & 0x7FF


def __idx_to_type(idx):
    idx = ((idx & 0x3FF) << 2) | 0x4000 if idx & 0x400 else idx << 4
    return idx & 0x7FFF


def __load_affinities():
    user_defined_affinities = load(open(join(dirname(__file__), "gc_type_affinities.json"), "r"))
    data, rows, cols = [], [], []

    # Default affinities


    # RESERVED type affinities


    # Add user defined affinities second as they may over-ride defaults.
    for i, affinity in enumerate(user_defined_affinities):
        if ok := affinity[0] < 0.0 or affinity > 1.0:
            __logger.warning("Affinity {} at entry {} ({}) out of bounds. 0.0 <= affinity <= 1.0. Ignoring.".format(
                affinity[0], i, affinity))
        for gc_type in affinity[1:]:
            if not __gc_type_validator(gc_type):
                __logger.warning("GCTD 0x{:04x}/{} at entry {} ({}) is invalid. Next log line gives details. Ignoring.".format(
                    gc_type, gc_type, i, affinity))
                __logger.warning("Invalid GCTD: {}".format(pformat(__gc_type_validator.errors)))
                ok = False
        if ok:
            data.append(affinity[0])
            rows.append(__type_to_idx(affinity[1]))
            cols.append(__type_to_idx(affinity[2]))
        
    return coo_matrix((data, (rows, cols)), dtype=float32)


__affinities = __load_affinities()


def affinity(gc_type_a, gc_type_b):
    """Return the affinity of gc_type_a to gc_type_b.

    Args
    ----
        gc_type_a (int): A Genetic Code Type Definition value.
        gc_type_b (int): A Genetic Code Type Definition value.


    Returns
    -------
        numpy.float32: The affinity of gc_type_a to gc_type_b.
    """
    if gc_type_a == gc_type_b: return float32(1.0)
    return __affinities[__type_to_idx(gc_type_a), __type_to_idx(gc_type_b)]
