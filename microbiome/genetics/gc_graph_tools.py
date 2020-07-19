'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/gc_graph_tools.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, July 19th 2020, 2:56:11 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from collections import Counter


# Tools for managing genetic code graphs

# Geneic code graphs have the following structure:
# [
#   [endpoint, row, type, shape, reference, referenced_by],
#   [endpoint, row, type, shape, reference, referenced_by],
#   [endpoint, row, type, shape, reference, referenced_by],
#   [endpoint, row, type, shape, reference, referenced_by],
#   ...
# ]


__ENDPOINT_IDX = 0
__ROW_IDX = 1
__TYPE_IDX = 2
__SHAPE_IDX = 3
__REF_IDX = 4
__REF_BY_IDX = 5


def __viable_input_rows(row):
    if row == 'A': return ('I', 'C')
    if row == 'B': return ('I', 'C', 'A')
    if row == 'O': return ('I', 'C', 'A', 'B')
    return tuple()


def __viable_input_types(typ):
    if typ == 'n': return ('i', 'f', 'n')
    return (typ,)


def __filter(filter_func, graph):
    return [n for n in filter(filter_func, graph)]


def src_filter(filter_func=lambda x: True):
    return lambda x: x[__ENDPOINT_IDX] and filter_func(x)


def dst_filter(filter_func=lambda x: True):
    return lambda x: not x[__ENDPOINT_IDX] and filter_func(x)


def row_filter(rows, filter_func=lambda x: True):
    return lambda x: any(map(lambda p: p == x[__ROW_IDX], rows)) and filter_func(x)


def type_filter(types, filter_func=lambda x: True, exact=True):
    __types = types if exact else set([x for y in types for x in __viable_input_types(y)])
    return lambda x: any(map(lambda p: p == x[__TYPE_IDX], __types)) and filter_func(x)


def shape_filter(shapes, filter_func=lambda x: True, exact=True):
    if exact: return lambda x: any(map(lambda p: p == x[__SHAPE_IDX], shapes)) and filter_func(x)
    return lambda x: any(map(lambda p: all(m <= n for m, n in zip (p, x[__SHAPE_IDX])), shapes)) and filter_func(x)


def ref_filter(ref):
    return lambda x: x[__REF_IDX] == ref


def ref_by_filter(ref_by, filter_func=lambda x: True):
    return lambda x: any(map(lambda p: p == ref_by, x[__REF_BY_IDX])) and filter_func(x)


def viable_src_filter(node, graph):
    return __filter(src_filter(row_filter(__viable_input_rows(node[__ROW_IDX]),
        type_filter(__viable_input_types(node[__TYPE_IDX]), shape_filter(node[__SHAPE_IDX])))), graph)


def viable_dst_filter(node, graph):
    return __filter(dst_filter(row_filter(__viable_input_rows(node[__ROW_IDX]),
        type_filter(__viable_input_types(node[__TYPE_IDX]), shape_filter(node[__SHAPE_IDX])))), graph)


def has_c(graph):
    return 'C' in [x[__ROW_IDX] for x in graph]


def has_b(graph):
    return 'B' in [x[__ROW_IDX] for x in graph]


def num_inputs(graph):
    return len(__filter(row_filter(('I',), graph)))


def num_outputs(graph):
    return len(__filter(row_filter(('O',), graph)))


def row_num_inputs(graph, row):
    return len(__filter(row_filter((row,), dst_filter()), graph))


def row_num_outputs(graph, row):
    return len(__filter(row_filter((row,), src_filter()), graph))


def next_reference(graph):
    refs = set([x[__REF_IDX] for x in graph])
    return min(set(range(max(refs) + 2)) - refs)


def validate(graph):
    error_list = []

    # General errors
    # FIXME: Walrus
    dupes = [i for i, c in Counter(graph).items() if c > 1]
    if dupes: error_list.append("References must be unique. Found duplicate references for {}.".format(dupes)) 

    # Connection consistency
    refs = [x[__REF_IDX] for x in graph]
    while refs:
        node_a = __filter(ref_filter(refs.pop()), graph)[0]
        for ref in node_a[__REF_BY_IDX]:
            node_b = __filter(ref_filter(ref), graph)[0]
            if node_a[__ENDPOINT_IDX] == node_b[__ENDPOINT_IDX]: error_list.append(
                "Nodes cannot be reference by the same end point type, {} is referenced by {} and both are {}.".format(
                    node_a[__REF_IDX], ref, ('destinations', 'sources')[node_a[__ENDPOINT_IDX]]))
            src, dst = (node_a, node_b) if node_a[__ENDPOINT_IDX] else (node_b, node_a)
            # FIXME: Walrus
            if not src[__TYPE_IDX] in __viable_input_types(dst[__TYPE_IDX]): error_list.append(
                "Node {} type is '{}' but its source node {} is type '{}' which is not one of {}".format(
                    dst[__REF_IDX], dst[__TYPE_IDX], src[__REF_IDX], src[__TYPE_IDX], __viable_input_types(dst[__TYPE_IDX])))
            if not src[__REF_IDX] in [x[__REF_IDX] for x in filter(src_filter(shape_filter([dst[__SHAPE_IDX]], exact=False)),graph)]:
                error_list.append("Node {} has shape {} but its source {} has shape {} which will not fit.".format(
                    dst[__REF_IDX], dst[__SHAPE_IDX], src[__REF_IDX], src[__SHAPE_IDX]))
            # FIXME: Walrus
            if not src[__ROW_IDX] in __viable_input_rows(dst[__ROW_IDX]):
                error_list.append("Source node {} is in row '{}' which is not valid for destination {} in row '{}'. Must be one of {}.".format(
                    src[__REF_IDX], src[__ROW_IDX], dst[__REF_IDX], dst[__ROW_IDX], __viable_input_rows(dst[__ROW_IDX])))

    # Input errors
    for node in filter(row_filter('I'), graph):
        if not node[__ENDPOINT_IDX]: error_list.append("All row 'I' nodes must be sources: {} is a destination.".format(node[__REF_IDX]))

    # Output errors
    has_output = False
    for node in filter(row_filter('O'), graph):
        if node[__ENDPOINT_IDX]: error_list.append("All row 'O' nodes must be destinations: {} is a source.".format(node[__REF_IDX]))
        has_output = True
    if not has_output: error_list.append("A graph must have at least one output node.")

    return error_list


def __coerce(graph, row, offset=0):
    new_graph = __filter(row_filter(('I', 'O')), graph)
    for node in new_graph:
        node[__ROW_IDX] = row
        # FIXME: Walrus
        node[__REF_IDX] = offset
        offset += 1 
    return new_graph


# This needs rethinking it is messy
def stack(graph_a, graph_b):
    graph = __filter(row_filter('I'), graph_a)
    for i, node in enumerate(graph): node[__REF_IDX] = i 
    graph = __coerce(graph_a, 'A', len(graph))
    graph.extend(__coerce(graph_b, 'B', len(graph)))
    for node in filter(dst_filter(row_filter(['B'])), graph):
        candidates = viable_src_filter(node, graph)
        if candidates:
            node[__REF_BY_IDX] = [candidate[0][__REF_IDX]]
        else:
            new_node = [
                True,
                'I',
                node[__TYPE_IDX],
                node[__SHAPE_IDX],
                next_reference(graph),
                [node[__REF_IDX]]
            ]
            graph.append(new_node)
