'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/binary_mutation_functions.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, June 21st 2020, 5:30:46 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''

# GC arguments can be modified by mutation functions


# field = 'I', 'C', 'A', 'B', 'O'
# f_offset = fractional offset 0.0 <= offset <= 1.0)
# Index into the gc['graph'] member lists 
def select(gc, field, f_offset):
    return round(len(gc['graph'][field]) * f_offset)


# src = 'I', 'C', 'A', 'B'
# dest = 'A', 'B', 'O'
# src_f_off = source list fractional offset
# dest_f_off = destination list fractional offset
# Connect a source vertex in the gc['graph'] to a destination vertex
def connect(gc, src, dest, src_f_off, dest_f_off):
    gc['graph'][dest][select(gc, dest, src_f_off)] = [src, select(gc, src, dest_f_off)]
    return gc


# Append c as a constant to gc['graph']
def append_constant(gc, c):
    if 'C' in gc['graph']:
        gc['graph']['C'].append(c)
    else:
        gc['graph']['C'] = [c]
    return gc


# f_offset = fractional offset in the gc['graph'] constsnt list
# factor = factor by with to multiple the constant
def mutate_constant(gc, f_offset, factor):
    if 'C' in gc['graph']: gc['graph']['C'][select(gc, 'C', f_offset)] * factor
    return gc


# Stack gca on gcb.
# This assumes gca and gcb have the same input and output definitions
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