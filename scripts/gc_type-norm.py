"""Normalise a genomic library entry JSON data file."""
#!/usr/bin/env python3

from json import load, dump
from sys import exit
from pprint import pformat
from argparse import ArgumentParser, FileType
from cerberus import Validator
from copy import deepcopy
from os.path import exists, join, dirname
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


def create_codon(i_types, o_type, inline, name, properties, code=None, imports=None):
    if o_type[0:2] == 'gc' or any([i[0:2] == 'gc' for i in i_types]):
        properties.update({'physical': True})
    codon = deepcopy(_GC_CODON_TEMPLATE)
    for n, i in enumerate(i_types): codon['graph']['A'].append(['I', n, gc_type_dict[i]['uid']])
    codon['meta_data']['name'] = name
    if not code is None: codon['meta_data']['function']['python3']['0']['code'] = code
    if not imports is None: codon['meta_data']['function']['python3']['0']['imports'] = imports
    codon['meta_data']['function']['python3']['0']['inline'] = inline
    codon['graph']['O'][0][2] = gc_type_dict[o_type]['uid']
    codon['properties'] = properties
    gc_codon_list.append(codon)


# When a type inherits properties from its parents certain rules apply:
#   1. If the child has multiple types it inherits the superset of the most relaxed rules.
#       e.g. A can be one of two types, P1 & P2, and has no 'min' key defined.
#            P1 has 'min' = 7
#            P2 has 'min' = 4
#            then A inherits the broadest restriction i.e. 'min' = 4
#       e.g. A can be one of two types P1 & P2.
#            A's 'ancestors' are the superset of {P1, P2} + P1['ancestors'] + P2['ancestors']
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
    if k == 'items':
        return None
    if k == 'ancestors':
        v1.extend(v2)
        return list(set(v1))
    print("Unexpected key = {}".format(k))
    assert False


def inherit(v):
    val = deepcopy(v)
    vv = {}

    # Types that have multiple parents do not inherit
    # They have the parents as ancestors but not the parents
    # ancestors as ancestors 
    #print(v)
    assert not isinstance(v['type'], list)
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
# Make sure the types type is in the ancestor list
validator = Validator(load(open("../microbiome/formats/gc_type_format.json", "r")))
for f in args.filename:
    for k, v in load(f).items():
        if not validator.validate(v):
            print(k, ': ', validator.errors)
            assert False
        gc_type_dict[k] = v
        if 'ancestors' in v:
            v['ancestors'].append(v['type'])
        else:
            v['ancestors'] = [v['type']]


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


# Number types
for i, val in enumerate(gc_type_dict.values(), 128):
    val['uid'] = i


# Create codons
for typ, val in gc_type_dict.items():

    # Random constant selections (per type)
    if 'allowed' in val:
        constant = create_constant(typ, val['allowed'])
        imports = [{'module': 'random', 'object': 'choice'}]
        create_codon(tuple(), typ, "random_choice({})".format(constant), "Random {} choice.".format(typ), {'deterministic': False}, imports=imports)

    # Lists with defined lengths & types
    if 'items' in val:

        # Create the list in one go
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

        # Get and set the list
        for i, c in enumerate(val['items']):
            if not 'allowed' in c:

                # Set
                code = "{i0}[" + str(i) + "] = {i1}"
                inline = "{i0}"
                create_codon((typ, c['type']), typ, inline, "Set {}[{}].".format(typ, i), {}, code)

                # Get
                inline = "{i0}[" + str(i) + "]"
                create_codon((typ,), c['type'], inline, "Get {}[{}].".format(typ, i), {})

    # Lists with variable lengths of a single type
    if val['type'] == 'list' and 'schema' in val:

        # Create
        inline = "[{i0}]"
        create_codon((val['schema']['type'],), typ, inline, "Create {}.".format(typ), {})

        # Append
        code = "{i0}.append({i1})"
        inline = "{i0}"
        create_codon((typ, val['schema']['type']), typ, inline, "Append to {}.".format(typ), {}, code)

        # Set
        code = "{i0}[{i1}] = {i2}"
        inline = "{i0}"
        create_codon((typ, typ + "_idx", val['schema']['type']), typ, inline, "Set {}[int].".format(typ), {}, code)

        # Get element
        inline = "{i0}[{i1}]"
        create_codon((typ, typ + "_idx"), val['schema']['type'], inline, "Get {}[int].".format(typ), {})

        # Get slice
        inline = "{i0}[{i1}:{i2}]"
        create_codon((typ, typ + "_idx", typ + "_idx"), typ, inline, "Get {}[int:int].".format(typ), {})

        # Clear
        code = "{i0}.clear()"
        inline = "{i0}"
        create_codon((typ,), typ, inline, "Clear {}.".format(typ), {}, code)

        # Pop
        inline = "{i0}.pop()"
        create_codon((typ,), val['schema']['type'], inline, "Pop from back {}.".format(typ), {})
        inline = "{i0}.pop(0)"
        create_codon((typ,), val['schema']['type'], inline, "pop from front {}.".format(typ), {})
        inline = "{i0}.pop({i1})"
        create_codon((typ, "int"), val['schema']['type'], inline, "Pop from [int] {}.".format(typ), {})

    # Dictionaries
    if val['type'] == 'dict':

        # Create the dictionary in one go.
        keys = []
        values = []
        for k, v in val['schema'].items():
            if not v.get('read-only', False):
                keys.append(k)
                values.append(v['type'])
        inline = "{{" + ", ".join(['"' + ky + '": {i' + str(n) + '}' for n, ky in enumerate(keys)]) + '}}'
        create_codon(values, typ, inline, "Create {}".format(typ), {})

        # Set a key-value pair
        for k, v in val['schema'].items():
            if not v.get('read-only', False):
                code = '{i0}["' + k + '"] = {i1}'
                inline = '{i0}'
                create_codon((typ, v['type']), v['type'], inline, "Set {}['{}']".format(typ, k), {}, code)

        # Get a value
        for k, v in val['schema'].items():
            inline = '{i0}["' + k + '"]'
            create_codon((typ,), v['type'], inline, "Get {}['{}']".format(typ, k), {})


#print(pformat(gc_constant_dict))

if exists("../microbiome/data/gc_types.json"):
    from microbiome.genetics.genomic_library_entry_validator import genomic_library_entry_validator
    nentries = []
    while gc_codon_list:
        codon = genomic_library_entry_validator.normalized(gc_codon_list.pop())
        if not genomic_library_entry_validator.validate(codon):
            print(genomic_library_entry_validator.errors)
            barf()
        nentries.append(codon)
    try:
        with open('gc_codons.json', 'w') as njsonfile:
            dump(nentries, njsonfile, indent=4, sort_keys=True)
    except Exception as e:
        print("ERROR: Unable to write JSON output file {} with error {}.".format(njsonfile, str(e)))


with open('gc_classes.py', 'w') as classfile:
    for t_name, t_def in gc_type_dict.items():
        if isinstance(t_def['type'], str):
            classfile.write("class {}({}): pass\n".format(t_name, t_def['type']))


# Convert all gc_type names to UIDs & preserve the name
def format_type(name, details):
    details['name'] = name
    if details['type'] != 'basic':
        details['type'] = gc_type_dict[details['type']]['uid']
    details['ancestors'] = [gc_type_dict[n]['uid'] for n in details.get('ancestors', []) if n != 'basic']
    return details


gc_type_json = {
    'v2n': {v['uid']: format_type(k, v) for k, v in gc_type_dict.items()},
    'n2v': {k:v['uid'] for k, v in gc_type_dict.items()}
    }
with open('gc_types.json', 'w') as njsonfile:
    dump(gc_type_json, njsonfile, indent=4, sort_keys=True)
