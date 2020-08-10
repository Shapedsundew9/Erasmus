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
    obj267:float32 = 0.0: An implicit conversion from a dictionary type to a float does not make sense.
"""


from numpy import float32, array, uint16
from json import load
from os.path import dirname, join
from logging import getLogger
from bitstruct import pack_dict, unpack_dict
from pprint import pformat
from re import split
from math import floor, log
from .gc_type_validator import gc_type_validator


__logger = getLogger(__name__)
__gc_type_validator = gc_type_validator(load(open(join(dirname(__file__), "../formats/gc_type_format.json"), "r")))
__gc_type_validator.allow_unknown = True
__BIT_FIELDS = {'fmt': 'b1u3u12', 'names': ('RESERVED', 'base_type', 'parameters')}
__BASE_TYPE = {'fmt': 'p13b1b1b1', 'names': ('object', 'float', 'integer')}
__NUMERIC_PARAM = {'fmt': 'p4b1u3u4b1b1u2', 'names': ('sign', 'log_size', 'n_dim', 'exact', 'RESERVED', 't_idx')}
__OBJECT_PARAM = {'fmt': 'p4u10u2', 'names': ('obj_id', 't_idx')}


def asint(gc_type):
    """Return an integer representation of a Genetic Code Type Definition.
    
    Args
    ----
        gc_type (dict/str): A Genetic Code Type Definition (see ref).

    Returns
    -------
        int: The integer value equivilent of gc_type.  
    """
    if isinstance(gc_type, int): return gc_type
    if isinstance(gc_type, str):
        if gc_type[0] == 'o': return (int(gc_type[3:]) << 2) + 0x4000
        if gc_type[0] == 'n': return 0x3f00
        value = 0x2008 if gc_type[0] == 'f' else 0x1008
        if gc_type[0] != 'u': value += 0x800
        return value + (int(log(int(split(r'(\d+)', gc_type)[1]), 2) - 3) << 8)

    bit_fields = {'base_type': int.from_bytes(pack_dict(**__BASE_TYPE, data=gc_type['base_type']), byteorder='big', signed=False)}
    param_def = __OBJECT_PARAM if gc_type['base_type']['object'] else __NUMERIC_PARAM
    bit_fields['parameters'] = int.from_bytes(pack_dict(**param_def, data=gc_type['parameters']), byteorder='big', signed=False)
    bit_fields['RESERVED'] = gc_type['RESERVED']
    return int.from_bytes(pack_dict(**__BIT_FIELDS, data=bit_fields), byteorder='big', signed=False)
        

def asdict(gc_type):
    """Return a dictionary representation of a Genetic Code Type Definition.
    
    Args
    ----
        gc_type (int/str): A Genetic Code Type Definition (see ref).

    Returns
    -------
        dict: A dictionary with keys and values defined by ref.  
    """
    if isinstance(gc_type, dict): return gc_type
    if isinstance(gc_type, str): return asdict(asint(gc_type))
    gc_type = gc_type & 0xFFFF
    definition = unpack_dict(**__BIT_FIELDS, data=gc_type.to_bytes(2, byteorder='big', signed=False))
    retval = {'base_type': unpack_dict(**__BASE_TYPE, data=definition['base_type'].to_bytes(2, byteorder='big', signed=False))}
    param_def = __OBJECT_PARAM if retval['base_type']['object'] else __NUMERIC_PARAM
    retval['parameters'] = unpack_dict(**param_def, data=definition['parameters'].to_bytes(2, byteorder='big', signed=False))
    retval['RESERVED'] = definition['RESERVED']
    return retval


def asstr(gc_type):
    """Return a string representation of a Genetic Code Type Definition.

    With the exception of 'numeric' string representations are limited to exact
    types. The n_dim & t_idx fields are ignored.

    Args
    ----
        gc_type (int/dict): A Genetic Code Type Definition (see ref).

    Returns
    -------
        str: A string representation of the type e.g. 'uint8', 'float64', 'obj234'  
    """
    if isinstance(gc_type, str): return gc_type
    if isinstance(gc_type, int): return asstr(asdict(gc_type))
    if gc_type['base_type']['object']: return 'obj' + str(gc_type['parameters']['obj_id'])
    idx = 2 * gc_type['base_type']['float'] + gc_type['base_type']['integer']
    type_str = ('int', 'float', 'numeric')[idx - 1]
    if not gc_type['parameters']['sign']: type_str = 'uint'
    if idx < 3: type_str += str(1 << (gc_type['parameters']['log_size'] + 3))
    return type_str


def validate(gc_type):
    """Validate a GCTD value.

    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if valid else False
    """
    retval = __gc_type_validator(asdict(gc_type))
    if not retval: __logger.debug("GCTD 0x{:04x} invalid: {}".format(gc_type, pformat(__gc_type_validator.errors)))
    return retval


def last_validation_error():
    """Return the dict of errors from the that call to validate().

    Returns
    -------
        dict: Dictionary of errors from the lat call to validate() 
    """
    return __gc_type_validator.errors


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
    value = asint(gc_type)
    return bool(value & 0x2000) and not bool(value & 0x1000)


def is_unsigned(gc_type):
    """Genetic Code Type Definition integer test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is an unsigned integer.
    """
    value = asint(gc_type)
    return not bool(value & 0x800) and bool(value & 0x1000)


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
    value = asint(gc_type)
    return bool(value & 0x2000) and not bool(value & 0x1000)


def is_numeric(gc_type):
    """Genetic Code Type Definition numeric test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is numeric. Returns False for all other types.  
    """
    value = asint(gc_type)
    return bool(value & 0x2000) and bool(value & 0x1000)


def is_object(gc_type):
    """Genetic Code Type Definition object test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is object else False.  
    """
    value = asint(gc_type)
    return bool(value & 0x4000)


def is_template(gc_type):
    """Genetic Code Type Definition template test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is templated else False.
    """
    value = asint(gc_type)
    return bool(value & 0x3)


def is_reserved_obj(gc_type):
    """Genetic Code Type Definition RESERVED object test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is a RESERVED object else False.
    """
    if not is_object(gc_type): return False
    return asdict(gc_type)['parameters']['obj_id'] < 128


def is_user_obj(gc_type):
    """Genetic Code Type Definition user defined object test.
    
    Args
    ----
        gc_type (int): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if the type is a user defined object else False.
    """
    if not is_object(gc_type): return False
    return asdict(gc_type)['parameters']['obj_id'] > 895


def __affinity_idx(gc_type_a, gc_type_b):
    a, b = asint(gc_type_a), asint(gc_type_b)
    mask_a = 0x7FFC if is_object(a) else 0x7FF0
    mask_b = 0x7FFC if is_object(b) else 0x7FF0
    return (a & mask_a) + ((b & mask_b) << 16)


def __load_affinities():
    user_defined_affinities = load(open(join(dirname(__file__), "gc_type_affinities.json"), "r"))
    affinities = {}

    # Default affinities
    pass

    # Add user defined affinities second as they may over-ride defaults.
    for i, affinity in enumerate(user_defined_affinities):
        if ok := affinity[2] < 0.0 or affinity > 1.0:
            __logger.warning("Affinity {} at entry {} ({}) out of bounds. 0.0 <= affinity <= 1.0. Ignoring.".format(
                affinity[2], i, affinity))
        for gc_type in map(asdict, affinity[0:2]):
            if not validate(gc_type):
                __logger.warning("GCTD 0x{:04x}/{} at entry {} ({}) is invalid. Ignoring.".format(gc_type, gc_type, i, affinity))
                ok = False
            if is_reserved_obj(gc_type):
                __logger.warning("GCTD 0x{:04x}/{} at entry {} ({}) specifies a RESERVED object. Ignoring.".format(gc_type, gc_type, i, affinity))
                ok = False
        if ok and not(affinity[0] == affinity[1] and affinity[2] == 1.0):
            affinities[__affinity_idx(affinity[0], affinity[1])] = float32(affinity[2])

    # RESERVED type affinities are last to prevent any accidental overrides by user definitions
    pass

    return affinities


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
    return __affinities[__affinity_idx(gc_type_a, gc_type_b)]
