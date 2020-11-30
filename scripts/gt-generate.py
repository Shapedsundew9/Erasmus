"""Generate Genetic Code Types.

'Standard' mathematical operations are tricky to implement because of the implicit type casting
behaviour. Whats more some operations do not result in the type you would necessarily expect.
This script executes the patrix of types for every operation inspecting the type of the result
for every successful one. Groups of permissable input & output types are also determined. 
For example:

    float + int = float
    float ** complex  = complex
    int << float = <exception> 

Mathematical operator codons can then be defined using input & output type groups
and translation functions.
"""
#!/usr/bin/env python3

import gc
from tqdm import tqdm
from os import getpid
from psutil import Process
from json import dump
from enum import IntEnum, unique
from copy import deepcopy
from pprint import pformat
from numpy import int8, int16, int32, int64, uint8, uint16, uint32, uint64, float32, float64, complex64, complex128

@unique
class category_idx(IntEnum):
    """Genetic Code Type category field values."""

    BASIC = 0x0
    TUPLE = 0x1
    SET = 0x2
    LIST = 0x3
    DICT = 0x4
    KEY_CONSTANT = 0x3D
    TYPE_GROUP = 0x3E
    TRANSLATION_FUNCTION = 0x3F

@unique
class k_type_idx(IntEnum):
    """Genetic Code Type k_type values."""

    NONE = 0x0
    BOOL = 0x1
    INT = 0x2
    FLOAT = 0x3
    COMPLEX = 0x4
    STR = 0x5

@unique
class np_scalar_type_idx(IntEnum):
    """Genetic Code Type e_type values for numpy scalar types."""

    INT8 = 0x10
    INT16 = 0x11
    INT32 = 0x12
    INT64 = 0x13
    UINT8 = 0x14
    UINT16 = 0x15
    UINT32 = 0x16
    UINT64 = 0x17
    FLOAT32 = 0x18
    FLOAT64 = 0x19
    COMPLEX64 = 0x1A
    COMPLEX128 = 0x1B

@unique
class np_array_type_idx(IntEnum):
    """Genetic Code Type e_type values for numpy scalar types."""

    ARRAY1 = 0x20
    ARRAY2 = 0x30
    ARRAY3 = 0x40

    """
    ARRAY4 = 0x50
    ARRAY5 = 0x60
    ARRAY6 = 0x70
    ARRAY7 = 0x80
    ARRAY8 = 0x90
    """


_GC_CODON_TEMPLATE = {
    "graph": {
        "A": [
            [
                "I",
                0,
                "To Be Defined"
            ],
            [
                "I",
                1,
                "To Be Defined"
            ]
        ],
        "O": [
            [
                "A",
                0,
                "To Be Defined"
            ]
        ]
    },
    "alpha_class": 0,
    "beta_class": 0,
    "properties": {},
    "meta_data": {
        "name": "To Be Defined",
        "function": {
            "python3": {
                "0": {
                    "inline": "To Be Defined"
                }
            }
        }
    }
}


# All python binary operators.
_OPERATORS = {
    '+': {
        'name': 'add',
        'inline': '{i0} + {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '-': {
        'name': 'subtract',
        'inline': '{i0} - {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '*': {
        'name': 'multiply',
        'inline': '{i0} * {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '/': {
        'name': 'true divide',
        'inline': '{i0} / {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '//': {
        'name': 'floor divide',
        'inline': '{i0} // {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '%': {
        'name': 'modulo',
        'inline': '{i0} % {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '@': {
        'name': 'matrix multiply',
        'inline': '{i0} @ {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '**': {
        'name': 'power',
        'inline': '{i0} ** {i1}',
        'properties': {
            'arithmetic': True,
            'deterministic': True
        }
    },
    '^': {
        'name': 'bitwise XOR',
        'inline': '{i0} ^ {i1}',
        'properties': {
            'bitwise': True,
            'deterministic': True
        }
    },
    '&': {
        'name': 'bitwise AND',
        'inline': '{i0} & {i1}',
        'properties': {
            'bitwise': True,
            'deterministic': True
        }
    },
    '|': {
        'name': 'bitwise OR',
        'inline': '{i0} | {i1}',
        'properties': {
            'bitwise': True,
            'deterministic': True
        }
    },
    '<<': {
        'name': 'left shift',
        'inline': '{i0} << {i1}',
        'properties': {
            'bitwise': True,
            'deterministic': True
        }
    },
    '>>': {
        'name': 'right shift',
        'inline': '{i0} >> {i1}',
        'properties': {
            'bitwise': True,
            'deterministic': True
        }
    }
}


def find_translation(f):
    match = False
    for translation, function in translation_function.items():
        if f == function['map']: 
            match = True 
            break
    assert match
    return translation


def find_group(t):
    match = False
    for group, gc_types in type_groups.items():
        if t == gc_types[0]: 
            match = True 
            break
    assert match
    return group


# This is experimental.
# We have lots of individual object but identical dictionaries in type_translation.
# This little routine finds all unique dictionaries and replaces duplicates with a reference.
# In theory memory should be less
# TODO: Have not measured that to be so. Need to validate the implementation.
def _compress_dict(d, record):
    for k, v in d.items():
        if isinstance(v, dict):
            _compress_dict(v, record)
            if not v in record:
                record.append(v)
            else:
                d[k] = record[record.index(v)]


def compress_dict(d):
    record = []
    _compress_dict(d, record)
    return record


# Define basic gc_types
# _*_TYPE = {gc_type_name: callable_class accept for 'None'}
# _V_TYPE is a superset of _K_TYPE including scalar and multi-dimensional numpy types.
_CATEGORY = {c.name.lower(): c for c in category_idx}
_K_TYPE = {k.name.lower(): (k, eval(k.name.lower())) for k in k_type_idx if k != k_type_idx.NONE}
_K_TYPE['none'] = (0, None)
_V_TYPE = deepcopy(_K_TYPE)
_V_TYPE.update({n.name.lower(): (n, eval(n.name.lower())) for n in np_scalar_type_idx})
for a in np_array_type_idx: _V_TYPE.update({''.join((n.name.lower(), a.name.lower())): (n + a - 0x10, None) for n in np_scalar_type_idx})


# Create dictionary lookups
#   {gc_type_name: gc_type_value}
#   {gc_type_value: gc_type_name}
gc_type_name_lookup = {}
for ck, cv in filter(lambda x: x[1] < 32, _CATEGORY.items()):
    for vk, vv in _V_TYPE.items():
        if cv == category_idx.DICT:
            for kk, kv in _K_TYPE.items():
                gc_type_name_lookup['_'.join((ck, kk, vk))] = (cv << 26) + (kv[0] << 22) + vv[0]
        elif cv == category_idx.LIST or cv == category_idx.TUPLE:
            gc_type_name_lookup['_'.join((ck, vk))] = (cv << 26) + vv[0]
            for d in range(2, 4): # TODO: Can do up to 16
                gc_type_name_lookup['_'.join((ck + str(d), vk))] = (cv << 26) + ((d-1) << 22) + vv[0]
        elif cv == category_idx.BASIC:
            gc_type_name_lookup[vk] = (cv << 26) + vv[0]
        else:
            gc_type_name_lookup['_'.join((ck, vk))] = (cv << 26) + vv[0]
gc_type_value_lookup = {v: k for k, v in gc_type_name_lookup.items()}


# Determine the output type of all combinations of input types for all python operators.
# NB: Excluding the none and str basic python types.
# The input & output types of successful operations make sets of types in a type_groups list.
# The mapping of input types to output type for each successful operation is recorded in type_translation.
type_groups = []
type_translation = {}
for op in tqdm(_OPERATORS.keys(), desc='Translation functions'):
    type_translation[op] = {}
    i0_set = set()
    i1_set = set()
    o0_set = set()
    for k1, v1 in filter(lambda x: not x[0] in ('none', 'str'), _V_TYPE.items()):
        for k2, v2 in filter(lambda x: not x[0] in ('none', 'str'), _V_TYPE.items()):
            try:
                o0 = eval('v1[1](2) {} v2[1](2)'.format(op))
            except Exception as e:
                pass
            else:
                type_translation[op].setdefault(k1, {}).setdefault(k2, type(o0).__name__)
                i0_set.add(k1)
                i1_set.add(k2)
                o0_set.add(type(o0).__name__)
    if i0_set: type_groups.append(tuple(sorted(list(i0_set))))
    if i1_set: type_groups.append(tuple(sorted(list(i1_set))))
    if o0_set: type_groups.append(tuple(sorted(list(o0_set))))


# Identify all the unique sets of types and determine which are subsets of others.
# The resulting type_groups dictionary consists on a 'numeric0' superset and (typically)
# several intersecting subset groups numbered 1 to N. 
type_groups = sorted([set(g) for g in set(type_groups)], key=len, reverse=True) 
type_groups = {'numeric{}'.format(i): (v, set()) for i, v in enumerate(type_groups)}
for k1, v1 in type_groups.items():
    for k2, v2 in type_groups.items():
        if v1[0] < v2[0]:
            v2[1].add(k1)
type_groups = {k: tuple(v) for k, v in type_groups.items()}
type_groups_json = {k: {'types': sorted(list(v[0])), 'sub-groups': sorted(list(v[1]))} for k, v in type_groups.items()}
type_groups_json['any'] = {'types': ['any'], 'sub-groups': ['any']}
for i, k in enumerate(type_groups.keys()):
    gc_type_name_lookup[k] = (0x78 << 24) + i - 0x80000000
    gc_type_value_lookup[(0x78 << 24) + i - 0x80000000] = k
with open('gc_group_types.json', 'w') as file_ptr:
    dump(type_groups_json, file_ptr, indent=4, sort_keys=True)

compress_dict(type_translation)
translation_function = {}
i = 0
for k, i0 in type_translation.items():
    if i0 and i0 not in translation_function.values():
        translation_function['translation' + str(i & 0x3FFFF)] = {'map': i0, 'group': find_group(set([o0 for i1 in i0.values() for o0 in i1.values()]))}
        i += 1
with open('gc_translation_types.json', 'w') as file_ptr:
    dump(translation_function, file_ptr, indent=4, sort_keys=True)
for k in translation_function.keys():
    gc_type_name_lookup[k] = (0x7C << 24) + int(k.replace('translation', '')) - 0x80000000
    gc_type_value_lookup[gc_type_name_lookup[k]] = k


gc_list = []
for op, i0 in type_translation.items():
    if i0:
        i1_keys = [k for i1 in i0.values() for k in i1.keys()]
        gc = deepcopy(_GC_CODON_TEMPLATE)
        gc['graph']['A'][0][2] = find_group(set(i0.keys()))
        gc['graph']['A'][1][2] = find_group(set(i1_keys))
        gc['graph']['O'][0][2] = find_translation(i0)
        gc['properties'] = _OPERATORS[op]['properties']
        gc['meta_data']['name'] = _OPERATORS[op]['name']
        gc['meta_data']['function']['python3']['0']['inline'] = _OPERATORS[op]['inline']
        gc_list.append(gc)

with open('gc_codons.json', 'w') as file_ptr:
    dump(gc_list, file_ptr, indent=4, sort_keys=True)

# Add custom types here
gc_type_name_lookup['any'] = -133955585; gc_type_value_lookup[gc_type_name_lookup['any']] = 'any'
gc_type_name_lookup['gc'] = 256; gc_type_value_lookup[gc_type_name_lookup['gc']] = 'gc'

# Calculate the reverse mapping of type to groups it is in
gc_type_group_lookup = {}
for gt in gc_type_name_lookup:
    for group, value in type_groups.items():
        if gt in value[0]:
            if not gt in gc_type_group_lookup: gc_type_group_lookup[gt] = []
            gc_type_group_lookup[gt].append(group)

gc_type_lookup = {'name': gc_type_name_lookup, 'value': gc_type_value_lookup, 'group': gc_type_group_lookup}
with open('gc_types.json', 'w') as file_ptr:
    dump(gc_type_lookup, file_ptr, indent=4, sort_keys=True)
