"""Write out all the valid combinations or rows and row src types for gc_graph."""
from itertools import combinations
from pprint import pformat
from copy import deepcopy
from json import dump


"""The sets of valid source rows for any given rows destinations"""
src_rows = {
    'I': tuple(),
    'C': tuple(),
    'A': ('I', 'C'),
    'B': ('I', 'C', 'A'),
    'U': ('I', 'C', 'A', 'B'),
    'O': ('I', 'C', 'A', 'B'),
    'P': ('I', 'C', 'B'),
    'F': ('I')
}


"""Valid combinations of ICAB """
# Row A must have no input if it is not specified and B is defined.
valid_combinations = (
    ('C',),
    ('A',),
    ('B',),
    ('I', 'C'),
    ('I', 'A'),
    ('I', 'B'),
    ('C', 'A'),
    ('C', 'B'),
    ('A', 'B'),
    ('I', 'C', 'A'),
    ('I', 'C', 'B'),
    ('I', 'A', 'B'),
    ('C', 'A', 'B'),
    ('I', 'C', 'A', 'B')
)


"""All valid row letters"""
rows = ('I', 'C', 'F', 'A', 'B', 'U', 'O', 'P')


gc_types = {}


def add_new_type(new_type, srcs):
    gc_types[new_type] = {
        "type": "gc_row",
        "minlength": 1,
        "maxlength": 256,    
        "schema": {
            "type": "gc_srcs_" + ''.join(srcs),
        }
    }


# Add the src hierarchy
# All destination endpoints are decendents of gc_srcs_ICAB
# Ancestors include all srcs
for v in valid_combinations:
    src_str = ''.join(v)
    gc_types["gc_srcs_" + src_str] = {
        "type": "object",
        "ancestors": ["gc_srcs_" + ''.join(src) for src in valid_combinations]
    }


# The general row definition type.
# Every row in the graph meets this definition.
gc_types["gc_row"] = {
    "type": "list",
    "minlength": 1,
    "maxlength": 256,    
    "schema": {
        "type": "gc_srcs_ICAB",
    }
}


# Basic Combinations
for c in valid_combinations:
    schema = {}
    ca = list(c)
    if 'B' in c and not 'A' in c: ca.append('A') # Implicit A
    if 'C' in c: schema['C'] = {"type": "gc_constant_row", "read-only": False}
    for r in c:
        srcs = [s for s in src_rows[r] if s in ca]
        if srcs:
            new_type = "gc_row_" + ''.join(srcs)
            schema[r] = {"type": new_type, "read-only": False}
            add_new_type(new_type, srcs)
    new_type = "gc_row_" + ''.join(ca)
    schema['O'] = {"type": new_type, "read-only": False}
    add_new_type(new_type, c)
    gc_types['gc_graph_O' + ''.join(c)] = {
        "type": "gc_graph",
        "schema": schema
    }


# Add U row variants (which is every graph type)
for k, v in list(gc_types.items()):
    if 'graph' in k and ('I'in k or 'A' in k or 'B' in k):
        schema = deepcopy(v['schema'])
        schema['U'] = {"type": schema['O']['type'], "read-only": False}
        gc_types[k + 'U'] = {
            "type": "gc_graph",
            "schema": schema
        }


# Add FP row variants (which is every graph type with inputs)
for k, v in list(gc_types.items()):
    if 'graph' in k and 'I' in k:
        srcs = list(k.replace("gc_graph_O", ""))
        new_type = "gc_row_" + ''.join(srcs)
        schema = deepcopy(v['schema'])
        schema['F'] = {"type": "gc_row_I", "read-only": False}
        schema['P'] = deepcopy(schema['O'])
        gc_types[k + 'FP'] = {
            "type": "gc_graph",
            "schema": schema
        }


# Graph type row valid keys
gc_types["gc_graph_row_letter"] = {
    "type": "letter_uppercase",
    "allowed": ["I", "C", "A", "B", "O", "U", "F", "P"]
}


# Row C definition
gc_types["gc_constant_row"] = {
    "type": "list",
    "minlength": 1,
    "maxlength": 256,    
    "schema": {
        "type": "gc_constant"
    }
}


# Constant definition
gc_types["gc_constant"] = {
    "type": "list",
    "minlength": 2,
    "maxlength": 2,    
    "items": [
        {
            "type": "gc_type_int"
        },
        {
            "type": "str"
        }
    ]
}


# A Graph is any one of the graph types we have generated.
gc_types["gc_graph"] = {
    "type": "dict",
    "schema": {
        "C": {"type": "gc_constant_row", "read-only": False},
        "A": {"type": "gc_row_IC", "read-only": False},
        "B": {"type": "gc_row_ICA", "read-only": False},
        "O": {"type": "gc_row_ICAB", "read-only": False},
        "U": {"type": "gc_row_ICAB", "read-only": False},
        "F": {"type": "gc_row_I", "read-only": False},
        "P": {"type": "gc_row_ICAB", "read-only": False}
    }
}


with open('gc_graph_types.json', 'w') as njsonfile:
    dump(gc_types, njsonfile, indent=4, sort_keys=True)
