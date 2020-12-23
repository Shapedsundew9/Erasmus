"""Normalise a genomic library entry JSON data file."""
#!/usr/bin/env python3

from json import load, dump
from sys import exit
from pprint import pformat
from argparse import ArgumentParser, FileType
from cerberus import Validator
from copy import deepcopy
from numpy import int8, int16, int32, int64, uint8, uint16, uint32, uint64, float32, float64, complex64, complex128


gc_type_dict = {}
gc_constant_dict = {}
gc_codon_list = []


_GC_CODON_TEMPLATE = {
    "graph": {
        "A": [],
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


def create_constant(name, values):
    constant_name = ('_' + name).upper()
    gc_constant_dict[constant_name] = tuple(values)
    return constant_name


def create_codon(i_types, o_type, code, name, properties):
    codon = deepcopy(_GC_CODON_TEMPLATE)
    for n, i in enumerate(i_types): codon['graph']['A'].append(['I', n, i])
    codon['meta_data']['name'] = name
    codon['meta_data']['function']['python3']['0']['inline'] = code
    codon['graph']['O'][0][2] = o_type
    codon['properties'] = properties
    gc_codon_list.append(codon)


def restrict(v1, v2, k):
    if k == 'type': 
        return None
    if k == 'schema':
        return None
    if k == 'allowed':
        return None
    if k == 'minlength':
        return min((v1, v2))
    if k == 'maxlength':
        return max((v1, v2))
    if k == 'min':
        return min((v1, v2))
    if k == 'max':
        return max((v1, v2))
    if k == 'read-only': 
        assert v1 == v2
        return v1
    if k == 'validate':
        return None 
    if k == 'regex':
        return None 
    if k == 'default':
        return None 
    if k == 'types':
        return None 
    if k == 'cast_to':
        return None 
    if k == 'basic':
        return None 
    print("Unexpected key = {}".format(k))
    assert False


def inherit(v):
    val = deepcopy(v)
    vv = {}
    if isinstance(v['type'], list):
        vals = [inherit(gc_type_dict[typ]) for typ in v['type']]
        for vl in vals: val.update(vl)
        for key, value in val.items():
            for vl in vals: 
                if key in vl: vv[key] = restrict(value, vl[key], key)
    else:
        if v['type'] != 'object':
            vl = inherit(gc_type_dict[v['type']])
            for key, value in val.items():
                if key in vl: vv[key] = restrict(value, vl[key], key)
            else:
                vv = deepcopy(v)

    for key, value in vv.items():
        if not value is None:
            val[key] = value

    return val


parser = ArgumentParser(description='Create type dictionaries.')
parser.add_argument('-f', '--filename', type=FileType('r'), help='GC type JSON files.', nargs='*')
args = parser.parse_args()


# Collect all the type definitions into a single dictionary and do some rudamentory checks.
validator = Validator(load(open("../microbiome/formats/gc_type_format.json", "r")))
for f in args.filename:
    for k, v in load(f).items():
        if not validator.validate(v):
            print(k, ': ', validator.errors)
            assert False
        gc_type_dict[k] = v


# Create dictionary key types
for typ, val in tuple(gc_type_dict.items()):
    if val['type'] == 'dict':
        gc_type_dict[typ + '_key'] = {
            "type": "str",
            "allowed": list(val['schema'].keys())
        }


# Create list index types
for typ, val in tuple(gc_type_dict.items()):
    if val['type'] in ('list', 'tuple'):
        gc_type_dict[typ + '_idx'] = {
            "type": "int",
            "min": 0
        }
        if 'maxlength' in val:
            gc_type_dict[typ + '_idx']['max'] = val['maxlength'] - 1
        

# Inherit parent properties & set basic type
for typ, val in gc_type_dict.items():
    if typ != 'object': gc_type_dict[typ] = inherit(val)


# Create codons
for typ, val in gc_type_dict.items():

    # Random constant selections (per type)
    if 'allowed' in val:
        constant = create_constant(typ, val['allowed'])
        create_codon(tuple(), typ, "choice({})".format(constant), "Random {} choice.".format(typ), {'deterministic': False})

    # Lists with defined lengths & types
    if 'items' in val:
        inputs = [v['type'] for v in val['items'] if not 'allowed' in v]
        values = []
        i = 0
        for c in val['items']:
            if 'allowed' in c:
                assert len(c['allowed']) == 1
                if isinstance(c['allowed'][0], str):
                    values.append("'" + c['allowed'][0] + "'")
                else:
                    values.append(str(c['allowed'][0]))
            else:
                values.append("{i" + str(i) + "}")
                i += 1
        inline = "[" + ", ".join(values)  + "]" 
        create_codon(inputs, typ, inline, "Create {}.".format(typ), {})

    # Dictionaries
    if val['type'] == 'dict':

        # Create the dictionary in one go.
        keys = []
        values = []
        for k, v in val['schema'].items():
            if not v.get('read-only', False):
                keys.append(k)
                values.append(v['type'])
        inline = "{" + ", ".join(['"' + ky + '": {i' + str(n) + '}' for n, ky in enumerate(keys)]) + '}'
        create_codon(values, typ, inline, "Create {}".format(typ), {})

        # Set a key-value pair
        for k, v in val['schema'].items():
            if not v.get('read-only', False):
                inline = '{i0}["' + k + '"] = {i1}'
                create_codon((typ, v['type']), v['type'], inline, "Set {}['{}']".format(typ, k), {})

        # Get a value
        for k, v in val['schema'].items():
            inline = '{i0}["' + k + '"]'
            create_codon((typ,), v['type'], inline, "Get {}['{}']".format(typ, k), {})


#print(pformat(gc_constant_dict))
print(pformat(gc_codon_list))


