"""Tools for managing genetic code graphs.

Created Date: Sunday, July 19th 2020, 2:56:11 pm
Author: Shapedsundew9

Description: Genetic code graphs define how genetic codes are connected together. The gc_graph_tools module
defines the rules of the connectivity (the "physics") i.e. what is possible to observe or occur.
"""

from collections import Counter
from enum import IntEnum
from .gc_type import asstr, asint, compatible_types, validate, last_validation_error, affinity
from pprint import pformat
from copy import deepcopy
from ..text_token import text_token, register_token_code
from logging import getLogger
from .gc_type_definitions import *


_logger = getLogger(__name__)


register_token_code('E01000', 'A graph must have at least one output.')
register_token_code('E01001', '{ep_type} endpoint {ref} is not connected to anything.')
register_token_code('E01002', '{ep_type} endpoint {ref} does not have a valid type: {type_errors}.')
register_token_code('E01003', 'Row {row} does not have contiguous indices starting at 0: {indices}.')
register_token_code('E01004', 'The references to row {row} are not contiguous indices starting at 0: {indices}.')
register_token_code('E01005', 'Constant {ref} does not have a valid value ({value}) for type {type}.')
register_token_code('E01006', 'If row "F" is defined then row "P" must be defined.')
register_token_code('E01007', 'Endpoint {ref} must be a source.')
register_token_code('E01008', 'Endpoint {ref} must be a destination.')
register_token_code('E01009', 'Source endpoint {ref1} type {type1} is not compatible with destination endpoint {ref2} type {type2}.')
register_token_code('E01010', 'Destination endpoint {ref1} cannot be connected to source endpoint {ref2}.')
register_token_code('E01011', 'Destination endpoint {ref1} cannot be connected to source endpoint {ref2} when row "F" exists.')
register_token_code('E01012', 'Endpoint {ref1} cannot reference row B {ref2} if "F" is defined.')
register_token_code('E01013', 'Row "P" length ({len_p}) must be the same as row "O" length ({len_o}) when "F" is defined.')


class conn_idx(IntEnum):
    """Genomic library entry graph connection format index."""

    ROW = 0
    INDEX = 1
    TYPE = 2


class const_idx(IntEnum):
    """Genomic library entry graph constant row format index."""

    VALUE = 0
    TYPE = 1


class ref_idx(IntEnum):
    """REFERENCED_BY format index."""

    ROW = 0
    INDEX = 1


class ep_idx(IntEnum):
    """gc_graph internal graph endpoint format index."""

    EP_TYPE = 0
    ROW = 1
    INDEX = 2
    TYPE = 3
    REFERENCED_BY = 4
    VALUE = 5


def validate_value(value_str, gc_type):
    """Validate the executable string is a valid gc_type value.

    Args
    ----
        value_str (str): As string that when executed as the RHS of an assignment returns a value of gc_type
        gc_type (int/str/dict): A Genetic Code Type Definition (see ref).

    Returns
    -------
        bool: True if valid else False
    """
    _logger.debug("retval = isinstance({}, {})".format(value_str, asstr(gc_type)))
    try:
        retval = eval("isinstance({}, {})".format(value_str, asstr(gc_type)))
    except:
        return False
    return retval 


class gc_graph():
    """Manipulating Genetic Code Graphs.
    
    Genetic Code graphs are internally stored with the following structure:
    [
        [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY, VALUE],
        [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY],
        [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY],
        [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY, VALUE],
        ...
    ]
    
    Each list element defines an endpoint where:
    
        EP_TYPE (bool): True == source, False == Destination
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
        'P': ('I', 'C', 'B'),
        'F': ('I')
    }


    """All valid row letters"""
    rows = ('I', 'C', 'F', 'A', 'B', 'O', 'P')


    _logger = getLogger(__name__)


    def __init__(self, graph):
        """Convert graph to internal format if necessary.

        Args
        ----
            graph (list/dict): A Genetic Code graph.
        """
        self.graph = self.__convert_to_internal(graph) if isinstance(graph, dict) else graph
        self.errors = []
        

    def __convert_to_internal(self, graph):
        """Convert graph to internal format.

        The internal format allows quicker searching for parameters by type, endpoint type etc.
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
        for row, parameters in graph.items():
            for index, parameter in enumerate(parameters):
                if row != 'C':
                    retval[row + str(index) + 'd'] = [False, row, index, asint(parameter[conn_idx.TYPE]), [[*parameter[0:2]]]]
                    src = "".join(map(str, parameter[0:2])) + 's'
                    if src in retval:
                        retval[src][ep_idx.REFERENCED_BY].append([row, index])
                    else:
                        retval[src] = [True, parameter[0], parameter[1], asint(parameter[conn_idx.TYPE]), [[row, index]]]
                else:
                    retval[row + str(index) + 's'] = [True, row, index, asint(parameter[const_idx.TYPE]), [], parameter[const_idx.VALUE]]
        return list(retval.values())

    
    def application_graph(self):
        """Convert graph to Genomic Library Application format.

        Returns
        -------
            graph (dict): A Genetic Code graph in genomic library application format.
        """
        graph = {}
        for ep in filter(self.dst_filter(), self.graph):
            row = graph[ep[ep_idx.ROW]]
            if not row in graph: graph[row] = []
            graph[row].append([*row[ep_idx.REFERENCED_BY], row[ep_idx.TYPE]])
        for ep in filter(self.row_filter('C'), self.graph):
            if not 'C' in graph: graph['C'] = []
            graph['C'].append([row[ep_idx.VALUE], row[ep_idx.TYPE]])
        return graph


    def endpoint_filter(self, ep_type, filter_func=lambda x: True):
        """Define a filter that only returns endpoints which have endpoint type == ep_type.

        Args
        ----
            ep_type (bool): True == source, False == Destination
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return only endpoints with a type == ep_type.
        """
        return lambda x: x[ep_idx.EP_TYPE] == ep_type and filter_func(x)


    def src_filter(self, filter_func=lambda x: True):
        """Define a filter that only returns endpoints of source type.

        Args
        ----
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return only source endpoints.
        """
        return lambda x: x[ep_idx.EP_TYPE] and filter_func(x)


    def dst_filter(self, filter_func=lambda x: True):
        """Define a filter that only returns endpoints of destination type.

        Args
        ----
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return only destination endpoints.
        """
        return lambda x: not x[ep_idx.EP_TYPE] and filter_func(x)


    def rows_filter(self, rows, filter_func=lambda x: True):
        """Define a filter that only returns endpoints in that are in a row in rows.

        Args
        ----
            rows (iter): An iterable of valid row labels i.e. in gc_graph.rows
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return endpoints in 'rows'.
        """
        return lambda x: any(map(lambda p: p == x[ep_idx.ROW], rows)) and filter_func(x)


    def row_filter(self, row, filter_func=lambda x: True):
        """Define a filter that only returns endpoints in that are in a specific row.

        Args
        ----
            row (string): A string from rows.
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return endpoints in 'row'.
        """
        return lambda x: x[ep_idx.ROW] == row and filter_func(x)


    def type_filter(self, gc_types, filter_func=lambda x: True, exact=True):
        """Define a filter that only returns endpoints with a gc_type in 'gc_types'.

        Args
        ----
            gc_types (iter): An iterable of valid gc_types
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.
            exact: If True only endpoints with types exactly matching 'gc_types'. If False types
            that have a non-zero affinity will also be returned.

        Returns
        -------
            (func): A function for a filter() that will return endpoints with qualifying 'gc_types'.
        """
        __types = gc_types if exact else set([x for y in gc_types for x in compatible_types(y)])
        return lambda x: any(map(lambda p: p == x[ep_idx.TYPE], __types)) and filter_func(x)


    def ref_filter(self, ref):
        """Define a filter that only returns the endpoint at ref.

        Args
        ----
            ref ([row, index]): A genetic code graph endpoint reference.

        Returns
        -------
            (func): A function for a filter() that will return the endpoint 'ref'.
        """
        return lambda x: x[ep_idx.ROW] == ref[ref_idx.ROW] and x[ep_idx.INDEX] == ref[ref_idx.INDEX] 


    def ref_by_filter(self, ref_by, filter_func=lambda x: True):
        """Define a filter that only returns the endpoints referenced by ref_by.

        Args
        ----
            ref_by (iter): An iterable of genetic code graph endpoint references [ROW, INDEX].

        Returns
        -------
            (func): A function for a filter() that will return the endpoints referenced by 'ref_by'.
        """
        return lambda x: any(map(lambda p: p == ref_by, x[ep_idx.REFERENCED_BY])) and filter_func(x)


    def viable_endpoint_filter(self, endpoint):
        """For a given connection endpoint in the graph row return a list of all viable connection endpoints.

        Viable endpoints must be of the opposite end point type, have a compatible type and be in a row
        that is permitted to connect.

        Args
        ----
            endpoint (endpoint): An endpoint in the graph internal representation.

        Returns
        -------
            (list): A list of viable endpoints.
        """
        return [n for n in filter(self.endpoint_filter(not endpoint[ep_idx.EP_TYPE], self.row_filter(gc_graph.src_rows[endpoint[ep_idx.ROW]],
            self.type_filter(endpoint[ep_idx.TYPE]))), self.graph)]


    def has_c(self):
        """Test if there are constants in the graph.

        Returns
        -------
            (bool): True if at least one constant is defined.
        """
        return 'C' in [x[ep_idx.ROW] for x in self.graph]


    def has_f(self):
        """Test if this is a flow control graph.

        Returns
        -------
            (bool): True if row 'F' is defined.
        """
        return 'F' in [x[ep_idx.ROW] for x in self.graph]


    def has_b(self):
        """Test if row B is defined in the graph.

        Returns
        -------
            (bool): True if row B exists.
        """
        return 'B' in [x[ep_idx.ROW] for x in self.graph]


    def num_inputs(self):
        """Return the number of inputs to the graph.

        Returns
        -------
            (int): The number of graph inputs.
        """
        return len(list(filter(self.row_filter('I'), self.graph)))


    def num_outputs(self):
        """Return the number of outputs from the graph.

        Returns
        -------
            (int): The number of graph outputs.
        """
        return len(list(filter(self.row_filter('O'), self.graph)))


    def row_num_inputs(self, row):
        """Return the number of inputs to a specific graph row.
        
        Note that the input row ('I') and constant row ('C') have no inputs.
        In both cases 0 will be returned.

        Args
        ----
            row (string): A valid graph row i.e. in gc_graph.rows

        Returns
        -------
            (int): The number of inputs to the speficied graph row.
        """
        return len(list(filter(self.row_filter(row, self.dst_filter()), self.graph)))


    def row_num_outputs(self, row):
        """Return the number of outputs to a specific graph row.
        
        Note that the output row ('O') and the flow row ('F') have no outputs.
        In both cases 0 will be returned.

        Args
        ----
            row (string): A valid graph row i.e. in gc_graph.rows
            
        Returns
        -------
            (int): The number of outputs to the speficied graph row.
        """
        return len(list(filter(self.row_filter(row, self.src_filter()), self.graph)))


    def validate(self, codon=False):
        """Check if the graph is valid.
        
        This function is not intended to be fast.
        Genetic code graphs MUST obey the following rules:
            1. Have at least 1 output in 'O'.
            2. All sources are connected.
            3. All destinations are connected.
            4. Types are valid.
            5. Indexes within are contiguous and start at 0.
            6. Constant values are valid.
            7. Row "P" is only defined if "F" is defined.
            8. Row A is defined if the graph is not for a codon.
            9. Row A is not defined if the graph is for a codon.
            10. All row 'I' endpoints are sources.
            11. All row 'O' & 'P' endpoints are destinations.
            12. Source types have a non-zero affinity to destination types.
            13. Rows destinations may only be connected to source rows as defined
                by gc_graph.src_rows.
            14. If row 'F' is defined:
                a. Row 'B' cannot reference row A.
                b. Row 'B' cannot be referenced in row 'O'.
                c. Row 'P' must have the same number of elements as row 'O'.

        Args
        ----
            codon (bool): Set to True if the graph is for a codon genetic code.
            
        Returns
        -------
            (bool): True if the graph is valid else False.
            If False is returned details of the errors found are in the errors member.
        """
        self.errors = []

        #1
        if self.num_outputs() == 0: self.errors.append(text_token({'E01000': {}}))

        #2 & #3
        for row in filter(lambda x: not len(x[ep_idx.REFERENCED_BY]), self.graph):
            self.errors.append(text_token({'E01001': {'ep_type': ['Destination', 'Source'][row[ep_idx.EP_TYPE]],
                'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #4
        for row in filter(lambda x: not validate(x[ep_idx.TYPE]), self.graph):
            self.errors.append(text_token({'E01002': {'ep_type': ['Destination', 'Source'][row[ep_idx.EP_TYPE]],
                'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'type_errors': last_validation_error()}}))

        #5
        ref_dict = {k: [] for k in gc_graph.rows}
        ep_dict = deepcopy(ref_dict)
        for row in self.graph:
            for ref in row[ep_idx.REFERENCED_BY]: ref_dict[ref[ref_idx.ROW]].append(ref[ref_idx.INDEX])
            ep_dict[row[ep_idx.ROW]].append(row[ep_idx.INDEX])
        gc_graph._logger.debug("ref_dict: {}".format(ref_dict))
        gc_graph._logger.debug("ep_dict: {}".format(ep_dict))
        for k, v in ref_dict.items():
            ep = ep_dict[k]
            if ep:
                if not (min(ep) == 0 and max(ep) == len(set(ep)) - 1):
                    self.errors.append(text_token({'E01003': {'row': k, 'indices': sorted(ep)}}))
            if v:
                if not (min(v) == 0 and max(v) == len(set(v)) - 1):
                    self.errors.append(text_token({'E01004': {'row': k, 'indices': sorted(v)}}))
        
        #6
        for row in filter(lambda x: x[ep_idx.ROW] == 'C' and not validate_value(x[ep_idx.VALUE], x[ep_idx.TYPE]), self.graph):
            self.errors.append(text_token({'E01005': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'value': row[ep_idx.VALUE],
                'type': asstr(row[ep_idx.TYPE])}}))

        #7
        if self.has_f() != bool(len(list(filter(self.row_filter('P'), self.graph)))):
                self.errors.append(text_token({'E01006': {}}))
    
        # 8 & 9
        # FIXME: It is not possible to tell from the graph whether this is a codon or not

        #10
        for row in filter(self.row_filter('I', self.dst_filter()), self.graph):
            self.errors.append(text_token({'E01007': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #11
        for row in filter(self.rows_filter(('O', 'P'), self.src_filter()), self.graph):
            self.errors.append(text_token({'E01008': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #12
        for row in filter(self.dst_filter(), self.graph):
            for ref in row[ep_idx.REFERENCED_BY]:
                src = next(filter(self.ref_filter(ref), self.graph))
                if affinity(src[ep_idx.TYPE], row[ep_idx.TYPE]) == 0.0:
                    self.errors.append(text_token({'E01009': {'ref1': [src[ep_idx.ROW], src[ep_idx.INDEX]], 'type1': asstr(src[ep_idx.TYPE]),
                        'ref2': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'type2': asstr(row[ep_idx.TYPE])}}))

        #13
        for row in filter(self.dst_filter(), self.graph):
            for ref in row[ep_idx.REFERENCED_BY]:
                if ref[ref_idx.ROW] not in gc_graph.src_rows[row[ep_idx.ROW]]:
                    self.errors.append(text_token({'E01010': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]],
                        'ref2': [ref[ref_idx.ROW], ref[ref_idx.INDEX]]}}))

        #14a
        if self.has_f():
            for row in filter(self.row_filter('B', self.dst_filter()), self.graph):
                for ref in filter(lambda x: x[ref_idx.ROW] == 'A', row[ep_idx.REFERENCED_BY]):
                    self.errors.append(text_token({'E01011': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]],
                        'ref2': [ref[ref_idx.ROW], ref[ref_idx.INDEX]]}}))

        #14b
        if self.has_f() and self.has_b():
            for row in filter(self.row_filter('O'), self.graph):
                for ref in row[ep_idx.REFERENCED_BY]:
                    if ref[ref_idx.ROW] == 'B':
                        self.errors.append(text_token({'E01012': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'ref2': ref}}))

        #14c
        if self.has_f():
            len_row_p = len(list(filter(self.row_filter('P'), self.graph)))
            if len_row_p != self.num_outputs():
                self.errors.append(text_token({'E01013': {'len_p': len_row_p, 'len_o': self.num_outputs()}}))

        return not self.errors
