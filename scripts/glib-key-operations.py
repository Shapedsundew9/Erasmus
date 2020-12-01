#!/usr/bin/env python3
"""Generate genomic library entry get and set codons."""

from json import load, dump
from sys import exit
from os import access, R_OK, system, W_OK
from os.path import isfile, isdir, join
from argparse import ArgumentParser
from pprint import pformat
from copy import deepcopy
from datetime import datetime
from microbiome.entry_column_meta_validator import entry_column_meta_validator
from microbiome.genetics.genomic_library_entry_validator import genomic_library_entry_validator
from microbiome.query_validator import query_validator
from microbiome.genetics.gc_type import validate

HEADER = '"""Genomic library entry access and genetic code type operations.\n\n' \
         'The file was generated by the glib-key-operations.py script on {}.' \
         '\n\n\n"""'.format(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

GC_TYPE_GET_CODON = {
    "graph": {
        "A": [
            [
                "I",
                0,
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
    "properties": {
        "physical": True,
        "deterministic": True
    },
    "meta_data": {
        "name": "Get {} {} field.",
        "function": {
            "python3": {
                "0": {
                    "inline": "To Be Defined"
                }
            }
        }
    }
}

GC_TYPE_SET_CODON = {
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
        ]
    },
    "properties": {
        "physical": True,
        "object_modify": True,
        "deterministic": True
    },
    "meta_data": {
        "name": "Set {} {} field.",
        "function": {
            "python3": {
                "0": {
                    "inline": "To Be Defined"
                }
            }
        }
    }
}

REQUIRED_FILES = (
    'genomic_library_entry_format.json',
    'gc_graph_format.json'
)

def generate_dict_codons(data, parent_type):
    codon_list = []
    for key, value in data.items():
        if 'gc_type' in value['meta']:
            codon = deepcopy(GC_TYPE_GET_CODON)
            codon['graph']['A'][0][2] = parent_type
            codon['graph']['O'][0][2] = value['meta']['gc_type']
            codon['meta_data']['name'] = codon['meta_data']['name'].format(parent_type, key)
            codon['meta_data']['function']['python3']['0']['inline'] = "{o0} = {i0}.get('" + key + "', None)"
            codon_list.append(codon)
            if value['meta']['settable']:
                codon = deepcopy(GC_TYPE_SET_CODON)
                codon['graph']['A'][0][2] = parent_type
                codon['graph']['A'][1][2] = value['meta']['gc_type']
                codon['meta_data']['name'] = codon['meta_data']['name'].format(parent_type, key)
                codon['meta_data']['function']['python3']['0']['inline'] = "{i0}['" + key + "'] = {i1}"
                codon_list.append(codon)
            if value['type'] == 'dict' and 'schema' in value:
                codon_list.extend(generate_dict_codons(value['schema'], value['meta']['gc_type']))
            if value['type'] == 'list' and 'schema' in value:
                codon_list.extend(generate_list_codons(value['schema'], value['meta']['gc_type']))
    return codon_list


def generate_list_codons(value, parent_type):
    codon_list = []
    if 'gc_type' in value['meta']:
        codon = deepcopy(GC_TYPE_GET_CODON)
        codon['graph']['A'][0][2] = parent_type
        codon['graph']['O'][0][2] = value['meta']['gc_type']
        codon['meta_data']['name'] = codon['meta_data']['name'].format(parent_type, key)
        codon['meta_data']['function']['python3']['0']['inline'] = "{o0} = {i0})"
        codon_list.append(codon)
        if value['meta']['settable']:
            codon = deepcopy(GC_TYPE_SET_CODON)
            codon['graph']['A'][0][2] = parent_type
            codon['graph']['A'][1][2] = value['meta']['gc_type']
            codon['meta_data']['name'] = codon['meta_data']['name'].format(parent_type, key)
            codon['meta_data']['function']['python3']['0']['inline'] += key + "'] = {i1}"
            codon_list.append(codon)
        if value['type'] == 'dict' and 'schema' in value:
            codon_list.extend(generate_dict_codons(value['schema'], value['meta']['gc_type']))
        if value['type'] == 'list'  and 'schema' in value and 'items' in value['schema']:
            codon_list.extend(generate_list_codons(value['schema']['items'], value['meta']['gc_type']))
    return codon_list


parser = ArgumentParser(description='Generate codons from genetic code type definitions.')
parser.add_argument('-d', '--directory', type=str, help='path to the format definition files.', default='.')
args = parser.parse_args()

if not isdir(args.directory):
    print("ERROR: Cannot find directory '{}'.".format(args.folder))
    exit()

if not access(args.directory, W_OK):
    print("ERROR: Current user does not have read-write access to directory '{}'.".format(args.folder))
    exit()

codon_list = []
for filename in map(lambda x: join(args.directory, x), REQUIRED_FILES):
    if not isfile(filename):
        print("ERROR: Cannot find {}.".format(filename))
        exit()

    if not access(filename, R_OK):
        print("ERROR: Cannot access {}.".format(filename))
        exit()

    try:
        with open(filename, 'r') as jsonfile:
            data = load(jsonfile)

    except Exception as e:
        print("ERROR: Unable to read JSON file {} with error {}.".format(args.filename, str(e)))
        exit()

    for key, value in data.items():
        error = False
        if not 'meta' in value:
            print("ERROR: No 'meta' definition for key {}.".format(key))
            error = True
        elif 'gc_type' in value['meta']:
            if not 'settable' in value['meta']:
                print("ERROR: No 'settable' definition for key {}.".format(key))
                error = True
            #if not validate(value['meta']['gc_type']):
            #    print("ERROR: No '{}' for key {} is not a valid genetic code type.".format(value['meta']['gc_type'], key))
            #    error = True
    if error: exit()
    codon_list.extend(generate_dict_codons(data, 'gc'))

with open(join(args.directory, REQUIRED_FILES[0]), 'r') as filename:
    print(filename)
    qv = query_validator(load(filename))
print(pformat(qv._validator.schema))
codon_list.extend(generate_dict_codons(qv._validator.schema, 'gc_query'))
    
nentries = []
while codon_list: nentries.append(genomic_library_entry_validator.normalized(codon_list.pop()))
try:
    with open(join(args.directory, 'codons_glib_operations.json'), 'w') as njsonfile:
        dump(nentries, njsonfile, indent=4, sort_keys=True)
except Exception as e:
    print("ERROR: Unable to write JSON output file {} with error {}.".format(njsonfile, str(e)))






