"""Tools for managing genetic code graphs

Created Date: Sunday, July 19th 2020, 2:56:11 pm
Author: Shapedsundew9
Description: Genetic code graphs define how genetic codes are connected together. The gc_graph_tools module
defines the rules of the connectivity (the "physics") i.e. what is possible to observe or occur. 
"""

from collections import Counter
from enum import Enum
from gc_type import asint, compatible_types


class conn_idx(Enum):
    """Genomic Library entry graph connection format index.
    """
    ROW = 0
    INDEX = 1
    TYPE = 2


class ref_idx(Enum):
    """REFERENCED_BY format index.
    """
    ROW = 0
    INDEX = 1


class row_idx(Enum):
    """gc_graph internal graph row format index.
    """
    ENDPOINT = 0
    ROW = 1
    INDEX = 2
    TYPE = 3
    REFERENCED_BY = 4
    VALUE = 5


class gc_row():
    """Row manipulation and analysis.
    FIXME: What is this all about
    """


    def __init__(self, ds_list):
        self.ds_list = ds_list


    def __ref_nums(self):
        return [ds[row_idx.INDEX][ref_idx.NUM] for ds in filter(lambda x: x[row_idx.ENDPOINT], self.ds_list)]


    def dest_type_list(self):
        return [ds[row_idx.TYPE] for ds in filter(lambda x: x[row_idx.ENDPOINT], self.ds_list)]


    def src_type_list(self):
        return [ds[row_idx.TYPE] for ds in filter(lambda x: not x[row_idx.ENDPOINT], self.ds_list)]


    def next_ref_num(self):
        ref_nums = set(self.__ref_nums())
        return min(set(range(max(ref_nums) + 2)) - ref_nums) 


    def validate(self):
        row = self.ds_list[0][row_idx.INDEX[ref_idx.ROW]]
        ref_num_counts = Counter(self.__ref_nums())
        errors = ["Reference {} appears {} times in row {}. A reference must be unique.".format(k, v, row) for k, v in ref_num_counts.items() if v > 1]
        return errors


class gc_graph():
    """Manipulating Genetic Code Graphs 
    
    Genetic Code graphs are internally stored with the following structure:
    [
        [ENDPOINT, ROW, INDEX, TYPE, REFERENCED_BY, VALUE],
        [ENDPOINT, ROW, INDEX, TYPE, REFERENCED_BY],
        [ENDPOINT, ROW, INDEX, TYPE, REFERENCED_BY],
        [ENDPOINT, ROW, INDEX, TYPE, REFERENCED_BY, VALUE],
        ...
    ]
    
    where:
    
        ENDPOINT (bool): True == source, False == Destination
        TYPE (gc_type): The gc_type of the end point
        INDEX (int): The index of the endpoint in the row. Note that the indices do not need to be contiguous just unique.
        REFERENCED_BY ([[ROW, INDEX]...]): A list of endpoints that connect to this endpoint.
        VALUE (obj): The value if the INDEX ROW is "C"

    This is easier to search and manipulate than the more compact format stored directly
    in the genetic code 'graph' field.
    """


    """The sets of valid source rows for any given rows destinations"""
    src_rows = {
        'A': ('I', 'C'),
        'B': ('I', 'C', 'A'),
        'O': ('I', 'C', 'A', 'B'),
        'F': ('I')
    }


    """All valid row letters"""
    __rows = ('I', 'C', 'F', 'A', 'B', 'O')


    def __init__(self, graph):
        """Convert graph to internal format if necessary.

        Args
        ----
            graph (list/dict): A Genetic Code graph.
        """
        self.graph = self.__convert_to_rows(graph) if isinstance(graph, dict) else graph
        self.errors = []
        

    def __convert_to_rows(self, graph):
        """Convert graph to internal format.

        The internal format allows quicker searching for parameters by type, endpoint etc.
        It maintains bi-directional references for quick manipulation.
        Types are stored in integer format for efficiency.

        Args
        ----
            graph (dict): A Genetic Code graph in genomic library application format.

        Returns
        -------
            (list): A Geneic Code graph in gc_graph internal list format.
        """
        retval = {}
        for row, parameters in graph:
            for index, parameter in enumerate(parameters):
                retval[row.join(str(index))][False, row, index, asint(parameter[conn_idx.TYPE]), [*parameter[0:2]]]
                src = "".join(parameter[0:2])
                if src in retval:
                    retval[src][row_idx.REFERENCED_BY].append([row, index])
                else:
                    retval[src] = [True, parameter[0], parameter[1], asint(parameter[conn_idx.TYPE]), [row, index]]
        return retval


    def endpoint_filter(self, endpoint, filter_func=lambda x: True):
        """Define a filter that only returns rows which have endpoint == 'endpoint'.

        Args
        ----
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return only 'endpoint' rows.
        """
        return lambda x: x[row_idx.ENDPOINT] == endpoint and filter_func(x)


    def src_filter(self, filter_func=lambda x: True):
        """Define a filter that only returns rows for source endpoints.

        Args
        ----
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return only source rows.
        """
        return lambda x: x[row_idx.ENDPOINT] and filter_func(x)


    def dst_filter(self, filter_func=lambda x: True):
        """Define a filter that only returns rows for destination endpoints.

        Args
        ----
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return only destination rows.
        """
        return lambda x: not x[row_idx.ENDPOINT] and filter_func(x)


    def row_filter(self, rows, filter_func=lambda x: True):
        """Define a filter that only returns rows in 'rows'.

        Args
        ----
            rows (iter): An iterable of valid row labels i.e. in gc_graph.__rows
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return rows in 'rows'.
        """
        return lambda x: any(map(lambda p: p == x[row_idx.ROW], rows)) and filter_func(x)


    def type_filter(self, gc_types, filter_func=lambda x: True, exact=True):
        """Define a filter that only returns rows with a gc_type in 'gc_types'.

        Args
        ----
            gc_types (iter): An iterable of valid gc_types
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.
            exact: If True only rows with types exactly matching 'gc_types'. If False types
            that have a non-zero affinity will also be returned.

        Returns
        -------
            (func): A function for a filter() that will return rows with qualifying 'gc_types'.
        """
        __types = types if exact else set([x for y in types for x in compatible_types(y)])
        return lambda x: any(map(lambda p: p == x[row_idx.TYPE], __types)) and filter_func(x)


    def ref_filter(self, ref):
        """Define a filter that only returns the row with where ROW, INDEX == 'ref'.

        Args
        ----
            ref ([row, index]): A genetic code graph endpoint reference.

        Returns
        -------
            (func): A function for a filter() that will return the row 'ref'.
        """
        return lambda x: x[row_idx.ROW] == ref[ref_idx.ROW] and x[row_idx.INDEX] == ref[ref_idx.INDEX] 


    def ref_by_filter(self, ref_by, filter_func=lambda x: True):
        """Define a filter that only returns the rows referenced by 'ref_by'.

        Args
        ----
            ref_by (iter): An iterable of genetic code graph endpoint references.

        Returns
        -------
            (func): A function for a filter() that will return the rows referenced by 'ref_by'.
        """
        return lambda x: any(map(lambda p: p == ref_by, x[row_idx.REFERENCED_BY])) and filter_func(x)


    def viable_endpoint_filter(self, row):
        """For a given connection endpoint in the graph ('row') return a list of all viable connection endpoints.

        Args
        ----
            row (row): A row in the graph.

        Returns
        -------
            (list): A list of viable endpoints (rows).
        """
        return [n for n in filter(endpoint_filter(not row[row_idx.ENDPOINT], row_filter(gc_graph.src_rows(row[row_idx.ROW]),
            type_filter(row[row_idx.TYPE]))), self.graph)]


    def has_c(self):
        """Test if there are constants in the graph.

        Returns
        -------
            (bool): True if at least one constant is defined.
        """
        return 'C' in [x[row_idx.ROW] for x in self.graph]


    def has_b(self):
        """Test if GCB is defined in the graph.

        Returns
        -------
            (bool): True if GCB is not the zero GC.
        """
        return 'B' in [x[row_idx.ROW] for x in self.graph]


    def num_inputs(self):
        """Return the number of inputs to the graph.

        Returns
        -------
            (int): The number of graph inputs.
        """
        return len([n for n in filter(row_filter(('I',)), self.graph)])


    def num_outputs(self):
        """Return the number of outputs from the graph.

        Returns
        -------
            (int): The number of graph outputs.
        """
        return len([n for n in filter(row_filter(('O',)), self.graph)])


    def row_num_inputs(self, row):
        """Return the number of inputs to a specific graph row.
        
        Note that the input row ('I') and constant row ('C') have no inputs.
        In both cases 0 will be returned.

        Args
        ----
            row (string): A valid graph row i.e. in gc_graph.__rows

        Returns
        -------
            (int): The number of inputs to the speficied graph row.
        """
        return len([n for n in filter(row_filter((row,), dst_filter()), self.graph)])


    def row_num_outputs(self, row):
        """Return the number of outputs to a specific graph row.
        
        Note that the output row ('O') and the flow row ('F') have no outputs.
        In both cases 0 will be returned.

        Args
        ----
            row (string): A valid graph row i.e. in gc_graph.__rows
            
        Returns
        -------
            (int): The number of outputs to the speficied graph row.
        """
        return len([n for n in filter(row_filter((row,), src_filter()), self.graph)])


    def next_index(self, row):
        """Return the next valid index for the given row.
        
        Indices are only required to be unique. The next valid index is
        the closest value to 0 that is not already an index in this row.

        Args
        ----
            row (string): A valid graph row i.e. in gc_graph.__rows
            
        Returns
        -------
            (int): The next valid index for this row.
        """
        refs = set([x[row_idx.INDEX] for x in filter(self.row_filter((row,)))])
        return min(set(range(max(refs) + 2)) - refs)


    def validate(self, codon=False):
        """Check if the graph is valid.
        
        Genetic code graphs MUST obey the following rules:
            1. Have at least 1 output
            2. All sources are connected
            3. All destinations are connected
            4. Types are valid
            5. Indexes within a row are unique
            6. Constant values are valid
            7. Destinations only have one source if row 'F' is not defined
            8. Row A is defined if the graph is not for a codon.
            9. Row A is not defined if the graph is fopr a codon.
            10. Rows destinations may only be connected to source rows as defined
                by gc_graph.src_rows.
            11. If row 'F' is defined:
                a. Row 'B' cannot reference row A
                b. If 'B' is defined any Output row endpoints referenced by 'B' must
                   also be referenced by one of 'A', 'I' or 'C'
                c. If 'B' is not defined any Output row endpoints referenced by 'A' 
                   must also be referenced by one of 'I' or 'C'

        Args
        ----
            row (string): A valid graph row i.e. in gc_graph.__rows
            
        Returns
        -------
            (int): The next valid index for this row.
        """
        destinations = [x[row_idx.ENDPOINT] for x in graph]
        while destinations:
            destination = destinations.pop()
            for source_ref in destination[row_idx.REFERENCED_BY]:
                source = next(filter(self.ref_filter(), self.ds_list))
                if : error_list.append(
                    "Nodes cannot be referenced by the same end point type, {} is referenced by {} and both are {}.".format(
                        node_a[__REF_IDX], ref, ('destinations', 'sources')[node_a[__ENDPOINT_IDX]]))
                src, dst = (node_a, node_b) if node_a[__ENDPOINT_IDX] else (node_b, node_a)
                # FIXME: Walrus
                if not src[__TYPE_IDX] in compatible_types(dst[__TYPE_IDX]): error_list.append(
                    "Node {} type is '{}' but its source node {} is type '{}' which is not one of {}".format(
                        dst[__REF_IDX], dst[__TYPE_IDX], src[__REF_IDX], src[__TYPE_IDX], compatible_types(dst[__TYPE_IDX])))
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
