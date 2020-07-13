'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/binary_mutation_functions.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, June 21st 2020, 5:30:46 pm
Author: Shapedsundew9


Copyright (c) 2020 Your Company
'''


from copy import deepcopy 


# GC arguments can be modified by mutation functions


# A general note:
#    1. Operations need to be balanced . If something is added another function needs to be able to take it 
#       away otherwise the system will explode one way or the other
#    2. It is not good to avoid exceptions and make functions no-ops. This will just add cruft to the
#       mutations. When the mutation is evolved any exception will be caught.
#  

# field = 'I', 'C', 'A', 'B', 'O', 'D'
# Return the number of times a field is referenced
def count_references_to(gc, field):
    count = 0
    for f in ('A', 'B', 'O'):
        if f in gc['graph']:
            for c in gc['graph'][f]:
                if c[0] == field:
                    count += 1
    return count


# Return a count of all the references
def total_references(gc):
    count = 0
    for f in ('A', 'B', 'O'):
        if f in gc['graph']:
            count += len(gc['graph'][f])
    return count


# field = 'I', 'C', 'A', 'B', 'O'
# f_offset = fractional offset 0.0 <= offset <= 1.0)
# Index into the gc['graph'] member lists 
def select(gc, field, f_offset):
    if field == 'I': return round((count_references_to(gc, 'I') - 1) * f_offset)
    return round((len(gc['graph'][field]) - 1) * f_offset)


# src = 'I', 'C', 'A', 'B'
# dest = 'A', 'B', 'O'
# src_f_off = source list fractional offset
# dest_f_off = destination list fractional offset
# Connect a source vertex in the gc['graph'] to a destination vertex
def connect(gc, src, dest, src_f_off, dest_f_off):
    gc['graph'][dest][select(gc, dest, src_f_off)] = [src, select(gc, src, dest_f_off)]
    return gc


# Append c as a constant to gc['graph'] if there are no supurflous constants already
# TODO: See if this can be speeded up by setting a flag rather than counting all the time
def append_constant(gc, c):
    if 'C' in gc['graph']:
        if count_references_to(gc, 'C') <= len(gc['graph']['C']): 
            if total_references(gc) < len(gc['graph']['C']):
                gc['graph']['C'].append(c)
    else:
        gc['graph']['C'] = [c]
    return gc


# Remove a constant if there is one.
# If the constant is referenced set the reference to 'D' (deleted)
# Adjust all other constant references so they remain the same.
def remove_constant(gc, offset):
    if len(gc['graph']['C']) == 1: 
        del gc['graph']['C']
        i = 0
    else:
        i = int(select(gc, 'C', offset))
        del gc['graph']['C'][i]
    for f in ('A', 'B', 'O'):
        if f in gc['graph']:
            for e in gc['graph'][f]:
                if e[0] == 'C':
                    if e[1] == i:
                        e[0] = 'D'
                    elif e[1] > i:
                        e[1] -= 1
    return gc


# Remove an input into one of the fields below by replacing the reference with 'D'
# field = 'A', 'B', 'O'
def remove_input(gc, field, offset):
    gc['graph']['field'][select(gc, field, offset)][0] = 'D'
    return gc


# f_offset = fractional offset in the gc['graph'] constsnt list
# factor = factor by with to multiple the constant
def mutate_constant(gc, f_offset, factor):
    gc['graph']['C'][select(gc, 'C', f_offset)] * factor
    return gc


# Stack gca on gcb.
def stack(gca, gcb):
    len_ai = len(gca['graph']['A'])
    len_ao = len(gca['graph']['O'])
    len_bi = len(gcb['graph']['A'])
    len_bo = len(gcb['graph']['O'])
    ai = [['I', i] for i in range(len_ai)]
    if len_ao < len_bi:
        bi = [['A', i] for i in range(len_ao)]
        bi.extend([['I', i] for i in range(len_ao, len_bi)])
    else:
        bi = [['A', i] for i in range(len_bi)]
    oi = [['B', i] for i in range(len_bo)]
    if len_ao > len_bi: oi.extend([['A', i] for i in range([len_bi, len_ao])])
    return {
        "graph": {
            'A': ai,
            'B': bi,
            'O': oi
        },
        "gca": gca['signature'],
        "gcb": gcb['signature'],
        "meta": {
            "parents": [[gca['signature'], gcb['signature']]]
        }
    }