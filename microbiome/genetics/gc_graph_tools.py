"""Tools for managing genetic code graphs.

Created Date: Sunday, July 19th 2020, 2:56:11 pm
Author: Shapedsundew9

Description: Genetic code graphs define how genetic codes are connected together. The gc_graph_tools module
defines the rules of the connectivity (the "physics") i.e. what is possible to observe or occur.
"""

from collections import Counter
from enum import IntEnum
from .gc_type import asstr, asint, compatible_types, validate, last_validation_error, affinity, UNKNOWN_TYPE
from pprint import pformat
from copy import deepcopy
from ..text_token import text_token, register_token_code
from logging import getLogger
from .gc_type_definitions import *
from random import choice


_logger = getLogger(__name__)
SRC_EP = True
DST_EP = False


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

register_token_code('I01000', '"I" row endpoint appended of UNKNOWN type.')
register_token_code('I01001', '"I" row endpoint removed.')
register_token_code('I01100', '"A" source row endpoint appended of UNKNOWN type.')
register_token_code('I01101', '"A" source row endpoint removed.')
register_token_code('I01102', '"A" destination row endpoint appended of UNKNOWN type.')
register_token_code('I01103', '"A" destination row endpoint removed.')
register_token_code('I01200', '"B" source row endpoint appended of UNKNOWN type.')
register_token_code('I01201', '"B" source row endpoint removed.')
register_token_code('I01202', '"B" destination row endpoint appended of UNKNOWN type.')
register_token_code('I01203', '"B" destination row endpoint removed.')
register_token_code('I01302', '"O" row endpoint appended of UNKNOWN type.')
register_token_code('I01303', '"O" row endpoint removed.')
register_token_code('I01402', '"P" row endpoint appended of UNKNOWN type.')
register_token_code('I01403', '"P" row endpoint removed.')

register_token_code('I01900', 'No source endpoints in the list to remove.')


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


# TODO: Consider caching calculated results.
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
    
        EP_TYPE (bool): SRC_EP or DST_EP
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
        """Convert graph to internal format.

        Args
        ----
            graph (list/dict): A Genetic Code graph.
        """
        # TODO: Uses self.rows where appropriate to reduce the need for calculated results.
        self.rows = ({k: len(v) for k, v in graph.items()}, {})
        self.unconnected = ({}, {})
        self.graph = self.__convert_to_internal(graph)
        self.status = []


    def __hash_ref(self, ref, ep_type):
        return ref[0] + str(ref[1]) + 'ds'[ep_type]


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
                    retval[row + str(index) + 'd'] = [DST_EP, row, index, asint(parameter[conn_idx.TYPE]), [[*parameter[0:2]]]]
                    src = "".join(map(str, parameter[0:2])) + 's'
                    if src in retval:
                        retval[src][ep_idx.REFERENCED_BY].append([row, index])
                    else:
                        retval[src] = [SRC_EP, parameter[0], parameter[1], asint(parameter[conn_idx.TYPE]), [[row, index]]]
                        if not row in self.rows[SRC_EP]: self.rows[SRC_EP][row] = 0
                        self.rows[SRC_EP][row] = max((self.rows[SRC_EP][row], parameter[1]))
                else:
                    retval[row + str(index) + 's'] = [SRC_EP, row, index, asint(parameter[const_idx.TYPE]), [], parameter[const_idx.VALUE]]
                    if not row in self.rows[SRC_EP]: self.rows[SRC_EP][row] = 0
                    self.rows[SRC_EP][row] = max((self.rows[SRC_EP][row], index))
        return retval


    def __add_ep(self, ep):
        """Add an endpoint to the internal graph format structure.

        Args
        ----
            ep (list): An endpoint list structure to be added to the internal graph.
        """
        ep_type, ep_row = ep[ep_idx.EP_TYPE], ep[ep_idx.ROW]
        self.graph[ep_row + str(ep[ep_idx.INDEX]) + 'ds'[ep_type]] = ep
        if not ep_row in self.rows[SRC_EP]: self.rows[ep_type][ep_row] = 0
        ep[ep_idx.INDEX] = self.rows[ep_type][ep_row]
        self.rows[ep_type][ep_row] += 1
        if not ep[ep_idx.REFERENCED_BY]:
            if ep_row in self.unconnected[ep_type]:
                self.unconnected[ep_type][ep_row] += 1
            else:
                self.unconnected[ep_type][ep_row] = 1


    def __remove_ep(self, ep):
        """Remove an endpoint to the internal graph format structure.

        Only unreferenced endpoint can be removed.

        Args
        ----
            ep (list): An endpoint list structure to be removed from the internal graph.
        """
        if not ep[ep_idx.REFERENCED_BY]:
            ep_type, ep_row = ep[ep_idx.EP_TYPE], ep[ep_idx.ROW]
            del self.graph[ep_row + str(ep[ep_idx.INDEX]) + 'ds'[ep_type]]
            self.rows[ep_type][ep_row] -= 1
            self.unconnected[ep_type][ep_row] -= 1



    def application_graph(self):
        """Convert graph to Genomic Library Application format.

        Returns
        -------
            graph (dict): A Genetic Code graph in genomic library application format.
        """
        graph = {}
        for ep in filter(self.dst_filter(), self.graph.values()):
            row = graph[ep[ep_idx.ROW]]
            if not row in graph: graph[row] = []
            graph[row].append([*row[ep_idx.REFERENCED_BY], row[ep_idx.TYPE]])
        for ep in filter(self.row_filter('C'), self.graph.values()):
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


    def unreferenced_filter(self, filter_func=lambda x: True):
        """Define a filter that only returns unreferenced endpoints.

        Returns
        -------
            (func): A function for a filter() that will return unreferenced endpoints.
        """
        return lambda x: not x[ep_idx.REFERENCED_BY] and filter_func(x)


    def referenced_filter(self, filter_func=lambda x: True):
        """Define a filter that only returns referenced endpoints.

        Returns
        -------
            (func): A function for a filter() that will return referenced endpoints.
        """
        return lambda x: x[ep_idx.REFERENCED_BY] and filter_func(x)


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
            self.type_filter(endpoint[ep_idx.TYPE]))), self.graph.values())]


    def has_i(self):
        """Test if row I is defined in the graph.

        Returns
        -------
            (bool): True if row I exists.
        """
        return 'I' in self.rows[SRC_EP]


    def has_a(self):
        """Test if row A is defined in the graph.

        If not then this graph is for a codon. 

        Returns
        -------
            (bool): True if row A exists.
        """
        return 'A' in self.rows[SRC_EP]


    def has_c(self):
        """Test if there are constants in the graph.

        Returns
        -------
            (bool): True if at least one constant is defined.
        """
        return 'C' in self.rows[SRC_EP]


    def has_f(self):
        """Test if this is a flow control graph.

        Returns
        -------
            (bool): True if row 'F' is defined.
        """
        return 'F' in self.rows[DST_EP]


    def has_b(self):
        """Test if row B is defined in the graph.

        Returns
        -------
            (bool): True if row B exists.
        """
        return 'B' in self.rows[SRC_EP]


    def num_inputs(self):
        """Return the number of inputs to the graph.

        Returns
        -------
            (int): The number of graph inputs.
        """
        return len(list(filter(self.row_filter('I'), self.graph.values())))


    def num_outputs(self):
        """Return the number of outputs from the graph.

        Returns
        -------
            (int): The number of graph outputs.
        """
        return len(list(filter(self.row_filter('O'), self.graph.values())))


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
        return len(list(filter(self.row_filter(row, self.dst_filter()), self.graph.values())))


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
        return len(list(filter(self.row_filter(row, self.src_filter()), self.graph.values())))


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
        self.messages = []

        #1
        if self.num_outputs() == 0: self.messages.append(text_token({'E01000': {}}))

        #2 & #3
        for row in filter(lambda x: not len(x[ep_idx.REFERENCED_BY]), self.graph.values()):
            self.messages.append(text_token({'E01001': {'ep_type': ['Destination', 'Source'][row[ep_idx.EP_TYPE]],
                'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #4
        for row in filter(lambda x: not validate(x[ep_idx.TYPE]), self.graph.values()):
            self.messages.append(text_token({'E01002': {'ep_type': ['Destination', 'Source'][row[ep_idx.EP_TYPE]],
                'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'type_errors': last_validation_error()}}))

        #5
        ref_dict = {k: [] for k in gc_graph.rows}
        ep_dict = deepcopy(ref_dict)
        for row in self.graph.values():
            for ref in row[ep_idx.REFERENCED_BY]: ref_dict[ref[ref_idx.ROW]].append(ref[ref_idx.INDEX])
            ep_dict[row[ep_idx.ROW]].append(row[ep_idx.INDEX])
        gc_graph._logger.debug("ref_dict: {}".format(ref_dict))
        gc_graph._logger.debug("ep_dict: {}".format(ep_dict))
        for k, v in ref_dict.items():
            ep = ep_dict[k]
            if ep:
                if not (min(ep) == 0 and max(ep) == len(set(ep)) - 1):
                    self.messages.append(text_token({'E01003': {'row': k, 'indices': sorted(ep)}}))
            if v:
                if not (min(v) == 0 and max(v) == len(set(v)) - 1):
                    self.messages.append(text_token({'E01004': {'row': k, 'indices': sorted(v)}}))
        
        #6
        for row in filter(lambda x: x[ep_idx.ROW] == 'C' and not validate_value(x[ep_idx.VALUE], x[ep_idx.TYPE]), self.graph.values()):
            self.messages.append(text_token({'E01005': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'value': row[ep_idx.VALUE],
                'type': asstr(row[ep_idx.TYPE])}}))

        #7
        if self.has_f() != bool(len(list(filter(self.row_filter('P'), self.graph.values())))):
                self.messages.append(text_token({'E01006': {}}))
    
        # 8 & 9
        # FIXME: It is not possible to tell from the graph whether this is a codon or not

        #10
        for row in filter(self.row_filter('I', self.dst_filter()), self.graph.values()):
            self.messages.append(text_token({'E01007': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #11
        for row in filter(self.rows_filter(('O', 'P'), self.src_filter()), self.graph.values()):
            self.messages.append(text_token({'E01008': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #12
        for row in filter(self.dst_filter(), self.graph.values()):
            for ref in row[ep_idx.REFERENCED_BY]:
                src = next(filter(self.ref_filter(ref), self.graph.values()))
                if affinity(src[ep_idx.TYPE], row[ep_idx.TYPE]) == 0.0:
                    self.messages.append(text_token({'E01009': {'ref1': [src[ep_idx.ROW], src[ep_idx.INDEX]], 'type1': asstr(src[ep_idx.TYPE]),
                        'ref2': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'type2': asstr(row[ep_idx.TYPE])}}))

        #13
        for row in filter(self.dst_filter(), self.graph.values()):
            for ref in row[ep_idx.REFERENCED_BY]:
                if ref[ref_idx.ROW] not in gc_graph.src_rows[row[ep_idx.ROW]]:
                    self.messages.append(text_token({'E01010': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]],
                        'ref2': [ref[ref_idx.ROW], ref[ref_idx.INDEX]]}}))

        #14a
        if self.has_f():
            for row in filter(self.row_filter('B', self.dst_filter()), self.graph.values()):
                for ref in filter(lambda x: x[ref_idx.ROW] == 'A', row[ep_idx.REFERENCED_BY]):
                    self.messages.append(text_token({'E01011': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]],
                        'ref2': [ref[ref_idx.ROW], ref[ref_idx.INDEX]]}}))

        #14b
        if self.has_f() and self.has_b():
            for row in filter(self.row_filter('O'), self.graph.values()):
                for ref in row[ep_idx.REFERENCED_BY]:
                    if ref[ref_idx.ROW] == 'B':
                        self.messages.append(text_token({'E01012': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'ref2': ref}}))

        #14c
        if self.has_f():
            len_row_p = len(list(filter(self.row_filter('P'), self.graph.values())))
            if len_row_p != self.num_outputs():
                self.messages.append(text_token({'E01013': {'len_p': len_row_p, 'len_o': self.num_outputs()}}))

        return not self.messages


    def random_mutation(self):
        """Randomly selects a way to mutate the graph and executes it.

        Mutations are single steps e.g. a disconnection of a source endpoint. The
        reconnection is a repair(). Compound changes are only permitted when
        there is only one possible repair option (excluding undoing the change) e.g.
        adding row 'F' requires that row 'P' must be added however, both rows endpoints
        may be connected many ways.

        Changes are likely to break the graph but they may not. For example,
        disconnecting a source end point will break it but change the type
        of an input source or the value of a constant may not.
        
        Each random change has the same probability:
            1. Add/remove a source end point.
            2. Add/remove a destination endpoint.
            3. Mutate the type of an endpoint.
            4. Mutate a constant.
            5. Add/remove 'F' (and 'P')

        """
        change_functions = (
            self.random_add_src_ep,
            self.random_remove_src_ep,
            self.random_add_dst_ep,
            self.random_remove_dst_ep,
            self.random_add_flow,
            self.random_remove_flow 
        )
        choice(change_functions)()
        

    def random_repair(self):
        """Randomly choose an error to attempt to repair.

        Repairs target specific errors and perform a single step repair attempt such as
        connecting a destination to a source. Compound repairs e.g. making a connection
        between an unconnected destination and unconnected source (which fixes two issues)
        may only happen by chance.

        Note that repairs in one graph may create issues in other graphs. For example adding
        an 'I' row input would break any G.C. instanciating the current one.

        Each possible repair to a graph error has the same probability:
            1. E01000: Randomly choose a viable source
            2. E01001: Randomly choose a viable source
            3. E01001: Randomly choose a viable destination
            4. 

        NB: E01002, E01004 to E01008 inclusive should never occur.  
        """
        pass


    def random_add_src_ep(self):
        """Randomly choose a source row and add an endpoint of unknown type."""
        src_rows = ['I', 'C', 'A']
        if self.has_b(): src_rows.append('B')
        self.add_src_ep(choice(src_rows))


    def add_src_ep(self, row):
        """Add an endpoint to row of UNKNOWN type.""" 
        self.__add_ep([SRC_EP, row, None, UNKNOWN_TYPE, []])
        if row == 'I': self.messages.append(text_token({'I01000': {}}))
        elif row == 'A': self.messages.append(text_token({'I01100': {}}))
        elif row == 'B': self.messages.append(text_token({'I01200': {}}))


    def random_remove_src_ep(self):
        """Randomly choose a source row and randomly remove an endpoint."""
        src_rows = [r for r in gc_graph.src_rows['O'] if r in self.rows[SRC_EP]]
        ep_list = self.unreferenced_filter(self.row_filter(choice(src_rows), self.src_filter()))
        self.remove_src_ep(tuple(choice(ep_list)))


    def remove_src_ep(self, ep_list):
        """Remove a source endpoint."""
        if ep_list:
            ep = ep_list[0]
            ep_row = ep[ep_idx.ROW]
            self.__remove_ep(ep)
            if ep_row == 'I': self.messages.append(text_token({'I01001': {}}))
            elif ep_row == 'A': self.messages.append(text_token({'I01101': {}}))
            elif ep_row == 'B': self.messages.append(text_token({'I01201': {}}))
        else:
            self.messages.append(text_token({'I01900': {}}))


    def random_add_dst_ep(self):
        """Randomly choose a destination row and add an endpoint of unknown type."""
        dst_rows = ['A', 'O']
        if self.has_b(): dst_rows.append('B')
        self.add_dst_ep(choice(dst_rows))


    def add_dst_ep(self, row):
        """Add an endpoint to row of UNKNOWN type.""" 
        self.__add_ep([DST_EP, row, None, UNKNOWN_TYPE, []])
        if row == 'O':
            self.messages.append(text_token({'I01302': {}}))
            if self.has_f():
                self.__add_ep([DST_EP, 'P', None, UNKNOWN_TYPE, []])
                self.messages.append(text_token({'I01402': {}}))
        elif row == 'A': self.messages.append(text_token({'I01102': {}}))
        elif row == 'B': self.messages.append(text_token({'I01202': {}}))


    def random_remove_dst_ep(self):
        """Randomly choose a destination row and randomly remove an endpoint."""
        dst_rows = ['A', 'O']
        if self.has_b(): dst_rows.append('B')
        ep_list = self.unreferenced_filter(self.row_filter(choice(dst_rows), self.dst_filter))
        self.remove_dst_ep(tuple(choice(ep_list)))


    def remove_dst_ep(self, ep_list):
        """Remove a destination endpoint."""
        if ep_list:
            ep = ep_list[0]
            ep_row = ep[ep_idx.ROW]
            self.__remove_ep(ep)
            if ep_row == 'O':
                self.messages.append(text_token({'I01303': {}}))
                if self.has_f():
                    ep[ep_idx.ROW] = 'P' 
                    self.__remove_ep(ep)
                    self.messages.append(text_token({'I01403': {}}))
            elif ep_row == 'A': self.messages.append(text_token({'I01103': {}}))
            elif ep_row == 'B': self.messages.append(text_token({'I01203': {}}))
        else:
            self.messages.append(text_token({'I01900': {}}))


    def random_remove_connection(self):
        """Randomly choose a connection and remove it."""
        self.remove_connection(list(filter(self.src_filter(self.referenced_filter), self.graph))[0])


    def remove_connection(self, src_ep, ep_filter=lambda x: x):
        """Remove connection to source from destination specified by ep_filter."""
        dst_ep_list = [self.graph[self.__hash_ref(ref, DST_EP)] for ref in src_ep[ep_idx.REFERENCED_BY]]
        dst_ep = list(filter(ep_filter, dst_ep_list))
        if dst_ep:
            dst_ep[ep_idx.REFERENCED_BY] = []
            dst_row = dst_ep[ep_idx.ROW]
            if not dst_row in self.unconnected[DST_EP]: self.unconnected[DST_EP][dst_row] = 0
            self.unconnected[DST_EP][dst_row] += 1
            src_ep[ep_idx.REFERENCED_BY].remove([dst_row, dst_ep[ep_idx.INDEX]])


    # TODO: Is this a GC level mutation?    
    def random_add_flow(self):
        """Is a placeholder."""
        pass

    
    # TODO: Is this a GC level mutation?    
    def random_remove_flow(self):
        """Is a placeholder."""
        pass

     




        



