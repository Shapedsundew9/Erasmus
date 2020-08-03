'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/gc_graph_tools.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, July 19th 2020, 2:56:11 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company

Description: Genetic code graphs define how genetic codes are connected together. The gc_graph_tools module
defines the rules of the connectivity (the "physics") i.e. what is possible to observe or occur. 
'''


from collections import Counter
from enum import Enum
from gc_type import select_dest, select_src


# Tools for managing genetic code graphs

# Genetic code graphs have the following structure:
# [
#   [ENDPOINT, TYPE, SHAPE, REFERENCE, REFERENCED_BY, VALUE],
#   [ENDPOINT, TYPE, SHAPE, REFERENCE, REFERENCED_BY],
#   [ENDPOINT, TYPE, SHAPE, REFERENCE, REFERENCED_BY],
#   [ENDPOINT, TYPE, SHAPE, REFERENCE, REFERENCED_BY, VALUE],
#   ...
# ]
# A REFERENCE or REFERENCED_BY is a list [ROW, NUM]
# Note that VALUE is only valid if REFERENCE[ROW] = C

class ref_idx(Enum):
    ROW = 0
    NUM = 1


class row_idx(Enum):
    ENDPOINT = 0
    ROW = 1
    TYPE = 2
    SHAPE = 3
    REFERENCE = 4
    REFERENCED_BY = 5
    VALUE = 6


class gc_row():
    '''
    Row manipulation and analysis.
    '''


    def __init__(self, ds_list):
        self.ds_list = ds_list


    def __ref_nums(self):
        return [ds[row_idx.REFERENCE][ref_idx.NUM] for ds in filter(lambda x: x[row_idx.ENDPOINT], self.ds_list)]


    def dest_type_list(self):
        return [ds[row_idx.TYPE] for ds in filter(lambda x: x[row_idx.ENDPOINT], self.ds_list)]


    def src_type_list(self):
        return [ds[row_idx.TYPE] for ds in filter(lambda x: not x[row_idx.ENDPOINT], self.ds_list)]


    def next_ref_num(self):
        ref_nums = set(self.__ref_nums())
        return min(set(range(max(ref_nums) + 2)) - ref_nums) 


    def validate(self):
        row = self.ds_list[0][row_idx.REFERENCE[ref_idx.ROW]]
        ref_num_counts = Counter(self.__ref_nums())
        errors = ["Reference {} appears {} times in row {}. A reference must be unique.".format(k, v, row) for k, v in ref_num_counts.items() if v > 1]
        return errors


class gc_graph():

    '''The sets of valid source rows for any given rows destinations'''
    __src_rows = {
        'A': ('I', 'C'),
        'B': ('I', 'C', 'A'),
        'O': ('I', 'C', 'A', 'B'),
        'F': ('I')
    }


    '''All valid row letters'''
    __rows = ('I', 'C', 'F', 'A', 'B', 'O')


    def __init__(self, graph):
        self.graph = graph
        for entry in filter(lambda x: isinstance(x[row_idx.TYPE], str), self.graph): entry[row_idx.TYPE] = ord(entry[row_idx.TYPE])




    def __filter(filter_func, graph):
        return [n for n in filter(filter_func, self.graph)]


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


    def validate():
        destinations = [x[row_idx.ENDPOINT] for x in graph]
        while destinations:
            destination = destinations.pop()
            for source_ref in destination[row_idx.REFERENCED_BY]:
                source = next(filter(self.ref_filter(), self.ds_list))
                if : error_list.append(
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


    # Coerce a graph into a row in a graph i.e. GCA or GCB
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
