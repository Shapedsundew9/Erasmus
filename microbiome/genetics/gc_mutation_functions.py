'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/binary_mutation_functions.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, June 21st 2020, 5:30:46 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''


def select(gc, f, c):
    return round(len(gc['graph'][f]) * c)


def connect(gc, c, s, d, cs, cd):
    gc['graph'][d][select(gc, d, cs)] = [s, select(gc, s, cd)]
    return gc


def append_constant(gc, c):
    if 'C' in gc['graph']:
        gc['graph']['C'].append(c)
    else:
        gc['graph']['C'] = [c]
    return gc


def mutate_constant(gc, c1, c2):
    if 'C' in gc['graph']: gc['graph']['C'][select(gc, 'C', c1)] * c2
    return gc


def stack(gca, gcb):
    return {
        "graph": {
            'A': gca['A'],
            'B': gca['O'],
            'O': gcb['O']
        },
        "gca": gca['signature'],
        "gcb": gcb['signature'],
        "meta": {
            "parents": [
                [gca['signature'], gcb['signature']]
            ]
        }
    }