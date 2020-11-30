"""Tools for managing genetic code graphs.

Created Date: Sunday, July 19th 2020, 2:56:11 pm
Author: Shapedsundew9

Description: Genetic code graphs define how genetic codes are connected together. The gc_graph_tools module
defines the rules of the connectivity (the "physics") i.e. what is possible to observe or occur.
"""

from collections import Counter
from enum import IntEnum
from .gc_type import validate, asint, compatible, asstr, member_of
from pprint import pformat
from copy import deepcopy, copy
from ..text_token import text_token, register_token_code
from logging import getLogger, DEBUG
from .gc_type_definitions import *
from random import choice
from graph_tool import Graph, Vertex, Edge
from graph_tool.draw import graph_draw
from math import pi
from cairo import FONT_WEIGHT_BOLD
from numpy import max as npmax


_logger = getLogger(__name__)
SRC_EP = True
DST_EP = False
DESTINATION_ROWS = ('A', 'B', 'F', 'O', 'P')
SOURCE_ROWS = ('I', 'C', 'A', 'B')


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
register_token_code('E01014', 'Row "U" endpoint {u_ep} referenced by more than one endpoint {refs}.')
register_token_code('E01015', 'Row "U" endpoint {u_ep} references a constant that does not exist {refs}.')

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
    {   str(ROW) + STR(INDEX) + str(EP_TYPE): [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY, VALUE],
        str(ROW) + STR(INDEX) + str(EP_TYPE): [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY],
        str(ROW) + STR(INDEX) + str(EP_TYPE): [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY],
        str(ROW) + STR(INDEX) + str(EP_TYPE): [EP_TYPE, ROW, INDEX, TYPE, REFERENCED_BY, VALUE],
        ...
    }

    Each list element defines an endpoint where:

        EP_TYPE (bool): SRC_EP or DST_EP
        TYPE (gc_type): The gc_type of the end point
        INDEX (int): The index of the endpoint in the row. Note that the indices do not need to be 
            contiguous just unique.
        REFERENCED_BY ([[ROW, INDEX]...]): A list of endpoints that connect to this endpoint.
        VALUE (obj): The value if the INDEX ROW is "C"

    This is easier to search and manipulate than the more compact format stored directly
    in the genetic code 'graph' field.
    """

    """The sets of valid source rows for any given rows destinations"""
    src_rows = {
        'A': ('I', 'C'),
        'B': ('I', 'C', 'A'),
        'U': ('I', 'C', 'A', 'B'),
        'O': ('I', 'C', 'A', 'B'),
        'P': ('I', 'C', 'B'),
        'F': ('I')
    }

    """All valid row letters"""
    rows = ('I', 'C', 'F', 'A', 'B', 'U', 'O', 'P')


    _logger = getLogger(__name__)


    def __init__(self, graph=None):
        """Convert graph to internal format.

        Args
        ----
            graph (list/dict): A Genetic Code graph.
        """
        # TODO: Uses self.rows where appropriate to reduce the need for calculated results.
        if graph is None: graph = {}
        self.rows = None
        self.app_graph = graph
        self.graph = self._convert_to_internal(graph)
        self.status = []


    def __repr__(self):
        """Print the graph in row order sources then destinations in index order."""
        str_list = []
        for row in gc_graph.rows:
            for ep_type in (False, True):
                row_dict = {k: v for k, v in self.graph.items() if v[0] == ep_type and v[ep_idx.ROW] == row}
                str_list.extend([k + ': ' + str(v) for k, v in sorted(row_dict.items(), key=lambda x:x[1][ep_idx.EP_TYPE])])
        string = ',\n'.join(str_list) + '\n'
        string += "(\n{},\n{}\n)\n{}".format(pformat(self.rows[0]), pformat(self.rows[1]), pformat(self.app_graph))
        string += "\nhas_a(): {}".format(self.has_a())
        string += "\nhas_b(): {}".format(self.has_b())
        string += "\nhas_c(): {}".format(self.has_c())
        string += "\nhas_f(): {}".format(self.has_f())
        string += "\nhas_i(): {}".format(self.has_i())
        return string


    #TODO: This function needs cleaning up. Maybe take an ep as an argument?
    def hash_ref(self, ref, ep_type):
        return ref[0] + str(ref[1]) + 'ds'[ep_type]


    def hash_ep(self, ep, ept=None):
        ept = 'ds'[ep[ep_idx.EP_TYPE]] if ept is None else ept 
        return ep[ep_idx.ROW] + str(ep[ep_idx.INDEX]) + ept


    def _convert_to_internal(self, graph):
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
        self.rows = ({}, {})
        for row, parameters in graph.items():
            for index, parameter in enumerate(parameters):
                if row != 'C':
                    # TODO: Make 0:2 a slice() constant
                    ep = [DST_EP, row, index, asint(parameter[conn_idx.TYPE]), [[*parameter[0:2]]]]
                    self.rows[DST_EP][row] = self.rows[DST_EP].get(row, 0) + 1
                    retval[self.hash_ep(ep)] = ep
                    src = self.hash_ref(ep[ep_idx.REFERENCED_BY][0], True)
                    if src in retval:
                        retval[src][ep_idx.REFERENCED_BY].append([row, index])
                    elif parameter[0] != 'C':
                        ref = [[row, index]] if row != 'U' else [] 
                        self.rows[SRC_EP][parameter[0]] = self.rows[SRC_EP].get(parameter[0], 0) + 1
                        retval[src] = [SRC_EP, parameter[0], parameter[1], asint(parameter[conn_idx.TYPE]), ref]
                else:
                    ep = [SRC_EP, row, index, asint(parameter[const_idx.TYPE]), [], parameter[const_idx.VALUE]]
                    self.rows[SRC_EP][row] = self.rows[SRC_EP].get(row, 0) + 1
                    retval[self.hash_ep(ep)] = ep
        return retval


    def _add_ep(self, ep):
        """Add an endpoint to the internal graph format structure.

        Args
        ----
            ep (list): An endpoint list structure to be added to the internal graph.
        """
        ep_type, ep_row = ep[ep_idx.EP_TYPE], ep[ep_idx.ROW]
        if not ep_row in self.rows[ep_type]: self.rows[ep_type][ep_row] = 0
        ep[ep_idx.INDEX] = self.rows[ep_type][ep_row]
        self.graph[self.hash_ep(ep)] = ep
        self.rows[ep_type][ep_row] += 1


    def _remove_ep(self, ep, check=True):
        """Remove an endpoint to the internal graph format structure.

        Only unreferenced endpoint can be removed.

        Args
        ----
            ep (list): An endpoint list structure to be removed from the internal graph.
        """
        if not check or not ep[ep_idx.REFERENCED_BY]:
            ep_type, ep_row = ep[ep_idx.EP_TYPE], ep[ep_idx.ROW]
            del self.graph[self.hash_ep(ep)]
            self.rows[ep_type][ep_row] -= 1


    def application_graph(self):
        """Convert graph to Genomic Library Application format.

        Returns
        -------
            graph (dict): A Genetic Code graph in genomic library application format.
        """
        graph = {}
        for ep in filter(self.dst_filter(), self.graph.values()):
            row = ep[ep_idx.ROW]
            if not row in graph: graph[row] = []
            if ep[ep_idx.REFERENCED_BY]: graph[row].append([*ep[ep_idx.REFERENCED_BY][0], ep[ep_idx.TYPE]])
        for ep in filter(self.row_filter('C'), self.graph.values()):
            if not 'C' in graph: graph['C'] = []
            graph['C'].append([ep[ep_idx.VALUE], ep[ep_idx.TYPE]])
        return graph


    def _gt_graph(self):
        """Create a graph_tool package graph."""
        g = Graph()
        vd = 60
        fill = {'I': [1.0, 1.0, 1.0, 1.0],
                'C': [0.5, 0.5, 0.5, 1.0],
                'F': [0.0, 1.0, 1.0, 1.0],
                'A': [1.0, 0.0, 0.0, 1.0],
                'B': [0.0, 0.0, 1.0, 1.0],
                'P': [0.0, 1.0, 0.0, 1.0],
                'O': [0.0, 0.0, 0.0, 1.0]
               }
        p = {'label': g.new_vertex_property('string'),
             'shape': g.new_vertex_property('string'),
             'rotation': g.new_vertex_property('float'),
             'text_rotation': g.new_vertex_property('float'),
             'fill': g.new_vertex_property('vector<float>'),
             'pos': g.new_vertex_property('vector<float>'),
             'size': g.new_vertex_property('int'),
             'font_size': g.new_vertex_property('int'),
             'font_weight': g.new_vertex_property('int'),
             'pen_width': g.new_edge_property('int'),
             'marker_size': g.new_edge_property('int')
            }
        pos = {'I': (1, 1),
               'C': (0, 1),
               'F': (2, 2),
               'A': (1, 2),
               'B': (0, 3),
               'P': (0, 4),
               'O': (1, 4),
              }
        gtg = {k: {'max_idx': int(npmax([rep[ep_idx.INDEX] for rep in filter(self.row_filter(k), self.graph.values())], initial=0))} for k in gc_graph.rows}
        width_0 = max((gtg['C']['max_idx'], gtg['B']['max_idx'], gtg['P']['max_idx']))
        width_1 = max((gtg['I']['max_idx'], gtg['A']['max_idx'], gtg['O']['max_idx']))
        for ep in self.graph.values():
            if ep[ep_idx.ROW] != 'U' and not ep[ep_idx.INDEX] in gtg[ep[ep_idx.ROW]]:
                v = g.add_vertex()
                gtg[ep[ep_idx.ROW]]['max_idx'] = max((ep[ep_idx.INDEX], gtg[ep[ep_idx.ROW]]['max_idx']))
                gtg[ep[ep_idx.ROW]][ep[ep_idx.INDEX]] = v
                p['label'][v] = ep[ep_idx.ROW] + str(ep[ep_idx.INDEX])
                p['fill'][v] = fill[ep[ep_idx.ROW]]
                if ep[ep_idx.ROW] in ('C', 'B', 'P'): x = 1 + ep[ep_idx.INDEX]
                if ep[ep_idx.ROW] in ('I', 'A', 'O'): x = width_0 + 2 + ep[ep_idx.INDEX]
                if ep[ep_idx.ROW] == 'F' : x = width_0 + width_1 + 3 + ep[ep_idx.INDEX]
                p['pos'][v] = [x, 2 * pos[ep[ep_idx.ROW]][1]]
                p['font_size'][v] = 14
                p['font_weight'][v] = FONT_WEIGHT_BOLD
                if self.hash_ref(ep[1:3], ep[ep_idx.EP_TYPE]) in self.graph and self.hash_ref(ep[1:3], not ep[ep_idx.EP_TYPE]) in self.graph: 
                    p['shape'][v], p['rotation'][v], p['text_rotation'][v], p['size'][v] = 'square', pi / 4, -pi / 4, vd
                elif ep[ep_idx.EP_TYPE] == SRC_EP:
                    p['shape'][v], p['rotation'][v], p['text_rotation'][v], p['size'][v] = 'triangle', pi, -pi, vd
                else:
                    p['shape'][v], p['rotation'][v], p['text_rotation'][v], p['size'][v] = 'triangle', 0.0, 0.0, vd
                
        for ep in filter(self.src_filter(), self.graph.values()):
            for ref in ep[ep_idx.REFERENCED_BY]:
                e = g.add_edge(gtg[ep[ep_idx.ROW]][ep[ep_idx.INDEX]], gtg[ref[ref_idx.ROW]][ref[ref_idx.INDEX]])
                p['pen_width'][e] = 4
                p['marker_size'][e] = 24
        return g, p, ((width_0 + width_1 + 5) * vd, vd * 5)


    def draw(self, name="graph"):
        """Draw the graph."""
        g, p, os = self._gt_graph()
        graph_draw(g, pos=p['pos'], vertex_text=p['label'], vertex_shape=p['shape'], vertex_rotation=p['rotation'],
            vertex_text_rotation=p['text_rotation'], vertex_fill_color=p['fill'],  vertex_size=p['size'],
            vertex_font_weight=p['font_weight'], vertex_font_size=p['font_size'], edge_pen_width=p['pen_width'], output=name+".png", 
            edge_marker_size=p['marker_size'], output_size=os)


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


    def src_row_filter(self, row, filter_func=lambda x: True):
        """Define a filter that only returns endpoints on source rows for the specified row.

        Args
        ----
            row (string): A destination row i.e. one of ('A', 'B', 'F', 'O', 'P')
            filter_func (func): A second filter to be applied. This allows *_filter methods
            to be stacked.

        Returns
        -------
            (func): A function for a filter() that will return only source endpoints.
        """
        if self.has_f():
            if row == 'B': src_rows = gc_graph.src_rows['A']
            elif row == 'O': src_rows = gc_graph.src_rows['B']
            else: src_rows = gc_graph.src_rows[row]
        else:
            src_rows = gc_graph.src_rows[row]
        
        return lambda x: x[ep_idx.EP_TYPE] and x[ep_idx.ROW] in src_rows and filter_func(x)


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
        _types = gc_types if exact else set([x for y in gc_types for x in member_of(y)])
        return lambda x: any(map(lambda p: p == x[ep_idx.TYPE], _types)) and filter_func(x)


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


    def _num_eps(self, row, ep_type):
        """Return the number of ep_type endpoints in row.
        
        If the effective logger level is DEBUG then a self consistency check is done.

        Args
        ----
        row (str): One of gc_graph.rows.
        ep_type (bool): DST_EP or SRC_EP

        Returns
        -------
        (int): Count of the specified endpoints.
        """
        if gc_graph._logger.getEffectiveLevel() == DEBUG:
            count = len(list(filter(self.row_filter(row, self.endpoint_filter(ep_type)), self.graph.values())))
            record = self.rows[ep_type].get(row, 0)
            if count != record:
                gc_graph._logger.fatal(
                    'Number of endpoints in row "{}" of gc_graph inconsistent: Counted {} recorded {}.'.format(
                    row, count, record))
                assert count == record
        return self.rows[ep_type].get(row, 0)


    def has_i(self):
        """Test if row I is defined in the graph.

        Returns
        -------
            (bool): True if row I exists.
        """
        return bool(self._num_eps('I', SRC_EP))


    def has_a(self):
        """Test if row A is defined in the graph.

        If not then this graph is for a codon. 

        Returns
        -------
            (bool): True if row A exists.
        """
        return bool(self._num_eps('A', SRC_EP)) or bool(self._num_eps('A', DST_EP))


    def has_c(self):
        """Test if there are constants in the graph.

        Returns
        -------
            (bool): True if at least one constant is defined.
        """
        return bool(self._num_eps('C', SRC_EP))


    def has_f(self):
        """Test if this is a flow control graph.

        Returns
        -------
            (bool): True if row 'F' is defined.
        """
        return bool(self._num_eps('F', DST_EP))


    def has_b(self):
        """Test if row B is defined in the graph.

        Returns
        -------
            (bool): True if row B exists.
        """
        return bool(self._num_eps('B', SRC_EP)) or bool(self._num_eps('B', DST_EP))


    def num_inputs(self):
        """Return the number of inputs to the graph.

        Returns
        -------
            (int): The number of graph inputs.
        """
        return self._num_eps('I', SRC_EP)


    def num_outputs(self):
        """Return the number of outputs from the graph.

        Returns
        -------
            (int): The number of graph outputs.
        """
        return self._num_eps('O', DST_EP)


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
        return self._num_eps(row, DST_EP)


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
        return self._num_eps(row, SRC_EP)


    def normalize(self):
        """Make the graph consistent.

        The make the graph consistent the following operations are performed:
            1. Connect all destinations to existing sources if possible
            2. Create new inputs for any destinations that are still unconnected.
            3. Purge any unconnected constants & inputs.
            4. Reference all unconnected sources in row 'U'
            5. self.app_graph is regenerated
        """

        #1
        self.connect_all()
        
        #2
        num_inputs = self.num_inputs()
        for ep in list(filter(self.dst_filter(self.unreferenced_filter()), self.graph.values())):
            new_input_ep = [SRC_EP, 'I', num_inputs, ep[ep_idx.TYPE], [[ep[ep_idx.ROW], ep[ep_idx.INDEX]]]]
            self._add_ep(new_input_ep)
            ep[ep_idx.REFERENCED_BY].append(['I', num_inputs])
            num_inputs += 1

        #3
        removed = False
        for ep in list(filter(self.rows_filter(('I', 'C'), self.unreferenced_filter()), self.graph.values())):
            removed = True
            self._remove_ep(ep)

        # If an I or C was removed then we have to ensure the indices of the remaining
        # endpoints are contiguous and start at 0. 
        if removed:
            # Make a list of all the indioces in I and C
            c_set = [ep[ep_idx.INDEX] for ep in filter(self.row_filter('C'), self.graph.values())]
            i_set = [ep[ep_idx.INDEX] for ep in filter(self.row_filter('I'), self.graph.values())]
            # Map the indices to a contiguous integer sequence starting at 0
            c_map = {idx: i for i, idx in enumerate(c_set)}
            i_map = {idx: i for i, idx in enumerate(i_set)}
            # For each row select all the endpoints and iterate through the references to them
            # For each reference update: Finf the reverse reference and update it with the new index
            # Finally update the index in the endpoint
            for row, r_map in {'I': i_map, 'C': c_map}.items():
                for ep in filter(self.row_filter(row), list(self.graph.values())):
                    for refs in ep[ep_idx.REFERENCED_BY]:
                        for refd in self.graph[self.hash_ref(refs, DST_EP)][ep_idx.REFERENCED_BY]:
                            if refd[ref_idx.ROW] == row and refd[ref_idx.INDEX] == ep[ep_idx.INDEX]:
                                refd[ref_idx.INDEX] = r_map[ep[ep_idx.INDEX]]
                    del self.graph[self.hash_ep(ep)]
                    ep[ep_idx.INDEX] = r_map[ep[ep_idx.INDEX]]
                    self.graph[self.hash_ep(ep)] = ep

        #4
        row_u_list = list(filter(self.row_filter('U'), self.graph.values()))
        for ep in row_u_list: self._remove_ep(ep, check=False)
        unreferenced = list(filter(self.src_filter(self.unreferenced_filter()), self.graph.values()))
        for i, ep in enumerate(unreferenced):
            self._add_ep([DST_EP, 'U', i, ep[ep_idx.TYPE], [[*ep[1:3]]]])

        #5
        self.app_graph = self.application_graph()


    def validate(self, codon=False):
        """Check if the graph is valid.
        
        This function is not intended to be fast.
        Genetic code graphs MUST obey the following rules:
            1. Have at least 1 output in 'O'.
            2. a. All sources are connected or referenced by the unconnected 'U' row.
               b. 'U' row endpoints may only be referenced once
               c. 'U' row cannot reference a non-existent constant
            3. All destinations are connected.
            4. Types are valid.
            5. Indexes within are contiguous and start at 0.
            6. Constant values are valid.
            7. Row "P" is only defined if "F" is defined.
            8. Row A is defined if the graph is not for a codon.
            9. Row A is not defined if the graph is for a codon.
            10. All row 'I' endpoints are sources.
            11. All row 'O' & 'P' endpoints are destinations.
            12. Source types are compatible with destination types.
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
        self.status = []

        #1
        if self.num_outputs() == 0: self.status.append(text_token({'E01000': {}}))

        #2a.
        for row in filter(self.src_filter(self.unreferenced_filter()), self.graph.values()):
            refs = [ep[ep_idx.REFERENCED_BY][0] for ep in filter(self.row_filter('U'), self.graph.values())]
            if not any([row[ep_idx.ROW] == r and row[ep_idx.INDEX] == i for r, i in refs]):
                self.status.append(text_token({'E01001': {'ep_type': ['Destination', 'Source'][row[ep_idx.EP_TYPE]],
                    'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #2b.
        for ep in filter(self.row_filter('U'), self.graph.values()):
            if len(ep[ep_idx.REFERENCED_BY]) > 1:
                self.status.append(text_token({'E01014': {'u_ep': [*ep[1:3]], 'refs': ep[ep_idx.REFERENCED_BY]}}))

        #2c.
        for ep in filter(self.row_filter('U'), self.graph.values()):
            if ep[ep_idx.REFERENCED_BY][0][ref_idx.ROW] == 'C':
                if not 'C' in self.app_graph or ep[ep_idx.REFERENCED_BY][0][ref_idx.INDEX] >= len(self.app_graph['C']):
                    self.status.append(text_token({'E01015': {'u_ep': [*ep[1:3]], 'refs': ep[ep_idx.REFERENCED_BY]}}))

        #3
        for row in filter(self.dst_filter(self.unreferenced_filter()), self.graph.values()):
            self.status.append(text_token({'E01001': {'ep_type': ['Destination', 'Source'][row[ep_idx.EP_TYPE]],
                'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #4
        for row in filter(lambda x: not validate(x[ep_idx.TYPE]), self.graph.values()):
            self.status.append(text_token({'E01002': {'ep_type': ['Destination', 'Source'][row[ep_idx.EP_TYPE]],
                'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'type_errors': 'Does not exist.'}}))

        #5
        ref_dict = {k: [] for k in gc_graph.rows}
        ep_dict = deepcopy(ref_dict)
        for row in self.graph.values():
            for ref in row[ep_idx.REFERENCED_BY]:
                ref_dict[ref[ref_idx.ROW]].append(ref[ref_idx.INDEX])
            ep_dict[row[ep_idx.ROW]].append(row[ep_idx.INDEX])
        gc_graph._logger.debug("ref_dict: {}".format(ref_dict))
        gc_graph._logger.debug("ep_dict: {}".format(ep_dict))
        for k, v in ref_dict.items():
            ep = ep_dict[k]
            if ep:
                if not (min(ep) == 0 and max(ep) == len(set(ep)) - 1):
                    self.status.append(text_token({'E01003': {'row': k, 'indices': sorted(ep)}}))
            if v:
                if not (min(v) == 0 and max(v) == len(set(v)) - 1):
                    self.status.append(text_token({'E01004': {'row': k, 'indices': sorted(v)}}))
        
        #6
        for row in filter(lambda x: x[ep_idx.ROW] == 'C' and not validate_value(x[ep_idx.VALUE], x[ep_idx.TYPE]), self.graph.values()):
            self.status.append(text_token({'E01005': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'value': row[ep_idx.VALUE],
                'type': asstr(row[ep_idx.TYPE])}}))

        #7
        if self.has_f() != bool(len(list(filter(self.row_filter('P'), self.graph.values())))):
                self.status.append(text_token({'E01006': {}}))
    
        # 8 & 9
        # FIXME: It is not possible to tell from the graph whether this is a codon or not

        #10
        for row in filter(self.row_filter('I', self.dst_filter()), self.graph.values()):
            self.status.append(text_token({'E01007': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #11
        for row in filter(self.rows_filter(('O', 'P'), self.src_filter()), self.graph.values()):
            self.status.append(text_token({'E01008': {'ref': [row[ep_idx.ROW], row[ep_idx.INDEX]]}}))

        #12
        for row in filter(self.dst_filter(), self.graph.values()):
            for ref in row[ep_idx.REFERENCED_BY]:
                try:
                    src = next(filter(self.src_filter(self.ref_filter(ref)), self.graph.values()))
                    if not compatible(asstr(src[ep_idx.TYPE]), asstr(row[ep_idx.TYPE])):
                        self.status.append(text_token({'E01009': {'ref1': [src[ep_idx.ROW], src[ep_idx.INDEX]], 'type1': asstr(src[ep_idx.TYPE]),
                            'ref2': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'type2': asstr(row[ep_idx.TYPE])}}))
                except StopIteration:
                    pass

        #13
        for row in filter(self.dst_filter(), self.graph.values()):
            for ref in row[ep_idx.REFERENCED_BY]:
                if ref[ref_idx.ROW] not in gc_graph.src_rows[row[ep_idx.ROW]]:
                    self.status.append(text_token({'E01010': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]],
                        'ref2': [ref[ref_idx.ROW], ref[ref_idx.INDEX]]}}))

        #14a
        if self.has_f():
            for row in filter(self.row_filter('B', self.dst_filter()), self.graph.values()):
                for ref in filter(lambda x: x[ref_idx.ROW] == 'A', row[ep_idx.REFERENCED_BY]):
                    self.status.append(text_token({'E01011': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]],
                        'ref2': [ref[ref_idx.ROW], ref[ref_idx.INDEX]]}}))

        #14b
        if self.has_f() and self.has_b():
            for row in filter(self.row_filter('O'), self.graph.values()):
                for ref in row[ep_idx.REFERENCED_BY]:
                    if ref[ref_idx.ROW] == 'B':
                        self.status.append(text_token({'E01012': {'ref1': [row[ep_idx.ROW], row[ep_idx.INDEX]], 'ref2': ref}}))

        #14c
        if self.has_f():
            len_row_p = len(list(filter(self.row_filter('P'), self.graph.values())))
            if len_row_p != self.num_outputs():
                self.status.append(text_token({'E01013': {'len_p': len_row_p, 'len_o': self.num_outputs()}}))

        if gc_graph._logger.getEffectiveLevel() == DEBUG:
            if self.status: gc_graph._logger.debug("Graph internal format:\n{}".format(self))
            for m in self.status: gc_graph._logger.debug(m)
            # Self consistency check.
            str(self)

        return not self.status


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
            self.random_remove_dst_ep
        )
        choice(change_functions)()
        

    def random_add_src_ep(self):
        """Randomly choose a source row and add an endpoint of unknown type."""
        src_rows = ['I', 'C', 'A']
        if self.has_b(): src_rows.append('B')
        self.add_src_ep(choice(src_rows))


    def add_src_ep(self, row):
        """Add an endpoint to row of UNKNOWN type.""" 
        self._add_ep([SRC_EP, row, None, UNKNOWN_TYPE, []])
        if row == 'I': self.status.append(text_token({'I01000': {}}))
        elif row == 'A': self.status.append(text_token({'I01100': {}}))
        elif row == 'B': self.status.append(text_token({'I01200': {}}))


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
            self._remove_ep(ep)
            if ep_row == 'I': self.status.append(text_token({'I01001': {}}))
            elif ep_row == 'A': self.status.append(text_token({'I01101': {}}))
            elif ep_row == 'B': self.status.append(text_token({'I01201': {}}))
        else:
            self.status.append(text_token({'I01900': {}}))


    def random_add_dst_ep(self):
        """Randomly choose a destination row and add an endpoint of unknown type."""
        dst_rows = ['A', 'O']
        if self.has_b(): dst_rows.append('B')
        self.add_dst_ep(choice(dst_rows))


    def add_dst_ep(self, row):
        """Add an endpoint to row of UNKNOWN type.""" 
        self._add_ep([DST_EP, row, None, UNKNOWN_TYPE, []])
        if row == 'O':
            self.status.append(text_token({'I01302': {}}))
            if self.has_f():
                self._add_ep([DST_EP, 'P', None, UNKNOWN_TYPE, []])
                self.status.append(text_token({'I01402': {}}))
        elif row == 'A': self.status.append(text_token({'I01102': {}}))
        elif row == 'B': self.status.append(text_token({'I01202': {}}))


    def random_remove_dst_ep(self):
        """Randomly choose a destination row and randomly remove an endpoint."""
        dst_rows = ['A', 'O']
        if self.has_b(): dst_rows.append('B')
        ep_list = self.unreferenced_filter(self.row_filter(choice(dst_rows), self.dst_filter))
        self.remove_dst_ep(tuple(choice(ep_list)))


    def remove_dst_ep(self, ep_list):
        """Remove a destination endpoint.
        
        Args
        ----
            ep_list (list): A list of destination endpoints. Only the first endpoint 
                            in the list will be removed.
        """
        if ep_list:
            ep = ep_list[0]
            ep_row = ep[ep_idx.ROW]
            self._remove_ep(ep)
            if ep_row == 'O':
                self.status.append(text_token({'I01303': {}}))
                if self.has_f():
                    ep[ep_idx.ROW] = 'P' 
                    self._remove_ep(ep)
                    self.status.append(text_token({'I01403': {}}))
            elif ep_row == 'A': self.status.append(text_token({'I01103': {}}))
            elif ep_row == 'B': self.status.append(text_token({'I01203': {}}))
        else:
            self.status.append(text_token({'I01900': {}}))


    def random_remove_connection(self):
        """Randomly choose a connection and remove it.
        
        This is done by first selecting a connection source endpoint then
        randomly (no filtering) choosing one of the connected destination
        endpoints.
        """
        src_ep_list = list(filter(self.src_filter(self.referenced_filter()), self.graph.values()))
        gc_graph._logger.debug("Selecting connection to remove from source endpoint list: {}".format(src_ep_list))
        if src_ep_list: self.remove_connection([choice(src_ep_list)])


    def remove_connection(self, src_ep_list, dst_ep_filter_func=lambda x: [choice(x)]):
        """Remove connection to source from destination specified by dst_ep_filter.

        Args
        ----
            src_ep_list (list): A list of source endpoints. Only the first endpoint 
                in the list will be removed.
            dst_ep_filter_func (func): A function that takes an endpoint list as the
                single argument and returns a filtered & sorted endpoint list. Only 
                the first endpoint will be used.  
        """
        if src_ep_list:
            src_ep = src_ep_list[0]
            dst_ep_list = [self.graph[self.hash_ref(ref, DST_EP)] for ref in src_ep[ep_idx.REFERENCED_BY]]
            if dst_ep_list:
                dst_ep_list = dst_ep_filter_func(dst_ep_list) 
                if dst_ep_list:
                    dst_ep = dst_ep_list[0] 
                    dst_ep[ep_idx.REFERENCED_BY] = []
                    dst_row = dst_ep[ep_idx.ROW]
                    src_ep[ep_idx.REFERENCED_BY].remove([dst_row, dst_ep[ep_idx.INDEX]])


    def random_add_connection(self):
        """Randomly choose two endpoints to connect.
        
        This is done by first selecting an unconnected destination endpoint then
        randomly (no filtering) choosing a viable source endpoint.
        """
        dst_ep_list = list(filter(self.unreferenced_filter(self.dst_filter()), self.graph.values()))
        gc_graph._logger.debug("Selecting connection to add to destination endpoint list: {}".format(dst_ep_list))
        if dst_ep_list: self.add_connection([choice(dst_ep_list)])


    def connect_all(self):
        """Connect all unconnected destination endpoints.
        
        Find all the unreferenced destination endpoints and connect them to a random viable source.
        If there is no viable source endpoint the destination endpoint will remain unconnected.
        """
        dst_ep_list = list(filter(self.unreferenced_filter(self.dst_filter()), self.graph.values()))
        for dst_ep in dst_ep_list: self.add_connection([dst_ep])


    def add_connection(self, dst_ep_list, src_ep_filter_func=lambda x: True):    
        """Add a connection to source from destination specified by src_ep_filter.

        Args
        ----
            dst_ep_list (list): A list of destination endpoints. Only the first endpoint 
                in the list that is unconnected will be connected.
            src_ep_filter_func (func): A function that takes an endpoint list as the
                single argument and returns a filtered & sorted endpoint list from which
                one source endpoint will be randomly chosen. 
        """
        if dst_ep_list:
            dst_ep = dst_ep_list[0]
            gc_graph._logger.debug("The destination endpoint: {}".format(dst_ep))
            src_ep_list = list(filter(self.src_filter(self.src_row_filter(dst_ep[ep_idx.ROW],
                self.type_filter([dst_ep[ep_idx.TYPE]], src_ep_filter_func, exact=False))), self.graph.values()))
            if src_ep_list:
                src_ep = choice(src_ep_list)
                gc_graph._logger.debug("The source endpoint: {}".format(src_ep))
                dst_ep[ep_idx.REFERENCED_BY] = [src_ep[1:3]]
                src_ep[ep_idx.REFERENCED_BY].append(dst_ep[1:3])
                return True
            gc_graph._logger.debug("No viable source endpoints for destination endpoint: {}".format(dst_ep))
        return False


    def stack(self, gB):
        """Stack this graph on top of graph gB.

        Graph gA (self) is stacked on gB to make gC i.e. gC inputs are gA's inputs
        and gC's outputs are gB's outputs:
            1. gC's inputs directly connect to gA's inputs, 1:1 in order
            2. gB's inputs preferentially connect to gA's outputs 1:1
            3. gB's outputs directly connect to gC's outputs, 1:1 in order
            4. Any gA's outputs that are not connected to gB inputs create new gC outputs
            5. Any gBs input that are not connected to gA outputs create new gC inputs

        Stacking only works if there is at least 1 connection from gA's outputs to gB's inputs.

        Args
        ----
        gB (gc_graph): Graph to sit on top of.

        Returns
        -------
        (gc_graph): gC.
        """
        # Create all the end points
        ep_list = []
        for ep in filter(gB.rows_filter(('I', 'O')), gB.graph.values()):
            row, idx, typ = ep[ep_idx.ROW], ep[ep_idx.INDEX], ep[ep_idx.TYPE]
            if row == 'I':
                ep_list.append([False, 'B', idx, typ, []])
                gB_has_I = True
            elif row == 'O':
                ep_list.append([True, 'B', idx, typ, [['O', idx]]])
                ep_list.append([False, 'O', idx, typ, [['B', idx]]])

        for ep in filter(self.rows_filter(('I', 'O')), self.graph.values()):
            row, idx, typ = ep[ep_idx.ROW], ep[ep_idx.INDEX], ep[ep_idx.TYPE]
            if row == 'I':
                ep_list.append([True, 'I', idx, typ, [['A', idx]]])
                ep_list.append([False, 'A', idx, typ, [['I', idx]]])
            elif row == 'O':
                ep_list.append([True, 'A', idx, typ, []])


        # Make a gC gc_graph object
        gC = gc_graph()
        for ep in ep_list: gC._add_ep(ep)

        # Preferentially connect A --> B but only 1:1
        gA_gB_connection = False
        for ep in filter(gC.dst_filter(gC.row_filter('B')), gC.graph.values()):
            gA_gB_connection = gA_gB_connection or gC.add_connection([ep], gC.row_filter('A', gC.unreferenced_filter()))

        if gA_gB_connection:
            # Extend O with any remaining A src's
            for ep in tuple(filter(gC.src_filter(gC.row_filter('A', gC.unreferenced_filter())), gC.graph.values())):
                idx = gC.num_outputs()
                gC._add_ep([DST_EP, 'O', idx, ep[ep_idx.TYPE], [['A', ep[ep_idx.INDEX]]]])
                ep[ep_idx.REFERENCED_BY].append(['O', idx])

            # Extend I with any remaining B dst's
            for ep in tuple(filter(gC.dst_filter(gC.row_filter('B', gC.unreferenced_filter())), gC.graph.values())):
                idx = gC.num_inputs()
                gC._add_ep([SRC_EP, 'I', idx, ep[ep_idx.TYPE], [['B', ep[ep_idx.INDEX]]]])
                ep[ep_idx.REFERENCED_BY].append(['I', idx])

            return gC
        return None




        



