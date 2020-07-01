'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_mutations.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Saturday, June 20th 2020, 6:54:47 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''


import pytest
from random import randint, random
from json import load
from microbiome.genetics.genomic_library_entry_validator import genomic_library_entry_validator
from logging import getLogger, basicConfig, DEBUG


basicConfig(filename='erasmus.log', level=DEBUG)
validator = genomic_library_entry_validator(load(open('./microbiome/formats/genomic_library_entry_format.json', "r")))


# TODO: For performance reasons this should just use a graph validator rather than a whole entry.
def entry_wrapper(graph):
    return {
        "graph": graph,
        "gca": "0" * 64 if not 'A' in graph else "1" * 64,
        "gcb": "0" * 64 if not 'B' in graph else "2" * 64,
        "generation": 1,
        "alpha_class": 0 if not 'A' in graph else 1,
        "beta_class": 2,
        "opt_num_codons": 1,
        "properties": {
            "unary_mutation": True
        },
        "meta_data": {
            "name": "Blah",
            "function": {
                "python3": {
                    "0": {
                        "inline": "Blah",
                        "callable": "Blah"
                    }
                }
            },
            "parents": [["3" * 64]]
        }
    }


def random_graph(max_inputs=12):
    graph = {'A': [], 'O': []}
    if random() < 0.5: graph['C'] = [random() for i in range(randint(1, round(max_inputs * 0.33)))]
    if random() < 0.95: graph['B'] = []
    for i in range(randint(1, max_inputs)):
        roll = random()
        if roll < 0.05: graph['O'].append(['I', i])
        elif 'B' in graph and roll < 0.37: graph['B'].append(['I', i])
        else: graph['A'].append(['I', i])
    for a in range(randint(1, round(max_inputs * 0.66))):
        roll = random()
        if roll < 0.37: graph['O'].append(['A', a])
        elif 'B' in graph: graph['B'].append(['A', a])
    for b in range(randint(1, round(max_inputs * 0.33))):
        if 'B' in graph: graph['O'].append(['B', b])
    if 'C' in graph:
        for c in range(len(graph['C'])):
            roll = random()
            if roll < 0.33: graph['A'].append(['C', c])
            elif 'B' in graph and roll < 0.67: graph['B'].append(['C', c])
            else: graph['O'].append(['C', c])
    if not graph['O']: graph['O'] = [['A', 0]]
    if 'B' in graph:
        found_b_output = False
        for r, i in graph['O']: found_b_output = found_b_output or r == 'B'
        if not found_b_output: graph['O'].append(['B', 0])
    keys = ('B', 'O') if 'B' in graph else ('O')
    found_a_output = False
    for pr in keys:
        for r, i in graph[pr]: found_a_output = found_a_output or r == "A" 
    if not found_a_output: graph['O'].append(['A', 0])
    return entry_wrapper(graph)



@pytest.mark.parametrize("iteration", list(range(1000)))
def test_random_graph(iteration):
    result = validator(random_graph())
    if not result: print(validator.document, validator.errors)
    assert result


