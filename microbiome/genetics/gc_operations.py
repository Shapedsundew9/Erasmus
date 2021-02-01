"""The operation that can be performed on a GC dictionary."""
from .genomic_library_entry_validator import NULL_GC, define_signature
from .gc_graph import gc_graph, ep_idx, ref_idx, SRC_EP, DST_EP, hash_ref, hash_ep
from random import getrandbits
from copy import deepcopy, copy
from logging import getLogger, DEBUG, INFO
from pprint import pformat


NULL_GC_TYPE = 0
_logger = getLogger(__name__)


def _copy_row(igc, rows, ep_type=None):
    """Copy the internal format definition of a row.

    If ep_type is None all endpoints regardless of end point type are copied.

    Args
    ----
    igc (dict): Internal gc_graph format gc_graph.
    rows (str): Valid row letters as a string e.g. 'IC'
    ep_type (bool): SRC_EP or DST_EP

    Returns
    -------
    (dict): An internal graph format dictionary containing the row.
    """
    if not ep_type is None:
        filter_func = lambda x: x[1][ep_idx.EP_TYPE] == ep_type and x[1][ep_idx.ROW] in rows
    else:
        filter_func = lambda x: x[1][ep_idx.ROW] in rows
    return {k: deepcopy(ep) for k, ep in filter(filter_func, igc.items())}


def _copy_clean_row(igc, rows, ep_type=None):
    """Copy the internal format definition of a row removing references.

    If ep_type is None all endpoints regardless of end point type are copied.

    Args
    ----
    igc (dict): Internal gc_graph format gc_graph.
    rows (str): Valid row letters as a string e.g. 'IC'
    ep_type (bool): SRC_EP or DST_EP

    Returns
    -------
    (dict): An internal graph format dictionary containing the clean row.
    """
    if not ep_type is None:
        filter_func = lambda x: x[1][ep_idx.EP_TYPE] == ep_type and x[1][ep_idx.ROW] in rows
    else:
        filter_func = lambda x: x[1][ep_idx.ROW] in rows
    copied_row = {k: copy(ep) for k, ep in filter(filter_func, igc.items())}
    for ep in copied_row.values(): ep[ep_idx.REFERENCED_BY] = []
    return copied_row


def _move_row(igc, src_row, src_ep_type, dst_row, dst_ep_type, clean=False):
    """Move a row definition to a different row.

    The endpoints moved are filtered by src_row & ep_type.
    If ep_type is None all endpoints regardless of end point type are moved.
    The moved rows are cleaned of references.

    Args
    ----
    igc (dict): Internal gc_graph format gc_graph.
    src_row (str): A valid row letter
    src_ep_type (bool or None): SRC_EP or DST_EP or None
    dst_row (str): A valid row letter
    dst_ep_type (bool or None): SRC_EP or DST_EP or None
    clean (bool): Remove references in dst_row if True

    Returns
    -------
    (dict): A gc_graph internal format containing the destination row endpoints.
    """
    if not src_ep_type is None:
        filter_func = lambda x: x[ep_idx.EP_TYPE] == src_ep_type and x[ep_idx.ROW] == src_row
    else:
        filter_func = lambda x: x[ep_idx.ROW] == src_row
    dst_eps = [deepcopy(ep) for ep in filter(filter_func, igc.values())]
    _logger.debug("Moving {} to row {} ep_type {}".format(dst_eps, dst_row, dst_ep_type))
    for ep in dst_eps:
        ep[ep_idx.ROW] = dst_row
        if clean: ep[ep_idx.REFERENCED_BY] = []
    if not dst_ep_type is None:
        for ep in dst_eps: ep[ep_idx.EP_TYPE] = dst_ep_type
    return {hash_ep(ep): ep for ep in dst_eps}


def _direct_connect(igc, src_row, dst_row):
    """Create dst_row and directly connect it to src_row.

    A direct connection means that dst_row has the same number, gc type and
    order of destination end points as src_row has source endpoints.
    src_row SRC_EPs should exist in fgc (else no-op).
    dst_row DST_EPs will be created in fgc.
    If any dst_row DST_EPs exist in fgc behaviour is undefined.

    Args
    ----
    igc (dict): Internal gc_graph format dict to be updated.
    src_row (str): 'I', 'C', 'A', or 'B'
    dst_row (str): Valid destination for src_row.

    Returns
    -------
    (dict): A gc_graph internal format containing the destination row endpoints.
    """
    connected_row = {}
    filter_func = lambda x: x[ep_idx.EP_TYPE] and x[ep_idx.ROW] == src_row
    for src_ep in tuple(filter(filter_func, igc.values())):
        dst_ep = [DST_EP, dst_row, src_ep[ep_idx.INDEX], src_ep[ep_idx.TYPE], [[src_row, src_ep[ep_idx.INDEX]]]] 
        connected_row[hash_ep(dst_ep)] = dst_ep            
    return connected_row


def _append_connect(igc, src_row, dst_row):
    """Append endpoints to dst_row and directly connect them to src_row.

    A direct connection means that dst_row has the same number, gc type and
    order of destination end points as src_row has source endpoints.
    src_row SRC_EPs should exist in fgc (else no-op).
    dst_row DST_EPs should exist in fgc.
    
    Args
    ----
    igc (dict): Internal gc_graph format dict to be updated.
    src_row (str): 'I', 'C', 'A', or 'B'
    dst_row (str): Valid destination for src_row.

    Returns
    -------
    (dict): A gc_graph internal format containing the destination row endpoints.
    """
    connected_row = {}

    # Find the next endpoint index in the destination row
    filter_func = lambda x: not x[ep_idx.EP_TYPE] and x[ep_idx.ROW] == dst_row
    next_idx = max([dst_ep[ep_idx.INDEX] for dst_ep in filter(filter_func, igc.values())]) + 1

    # Append a destination endpoint for every source endpoint
    filter_func = lambda x: x[ep_idx.EP_TYPE] and x[ep_idx.ROW] == src_row
    for src_ep in tuple(filter(filter_func, igc.values())):
        dst_ep = [DST_EP, dst_row, next_idx, src_ep[ep_idx.TYPE], [[src_row, src_ep[ep_idx.INDEX]]]] 
        connected_row[hash_ep(dst_ep)] = dst_ep
        next_idx += 1
    return connected_row


def _redirect_refs(igc, row, ep_type, old_ref_row, new_ref_row):
    """Redirects references on row from old_ref_row to new_ref_row.

    Args
    ----
    igc (dict): Internal gc_graph format dict to be updated.
    row (str): A valid row
    ep_type (bool): The old_ref_row ep_type.
    old_ref_row (str): A valid row
    new_ref_row (str): A valid row

    Returns
    -------
    (dict): Modified igc
    """
    filter_func = lambda x: x[ep_idx.EP_TYPE] == ep_type and x[ep_idx.ROW] == row
    for ep in filter(filter_func, igc.values()):
        for ref in ep[ep_idx.REFERENCED_BY]:
            if ref[ref_idx.ROW] == old_ref_row:
                ref[ref_idx.ROW] = new_ref_row
    return igc


def _insert_as(igc, row):
    """Create an internal gc_format dict with igc as row.

    Args
    ----
    igc (dict): Internal gc_graph format gc_graph.
    row (str): 'A' or 'B'

    Returns
    -------
    (dict): Internal gc_format dict with igc as row.
    """
    ret_val = {}
    for ep in filter(lambda x: x[ep_idx.ROW] in ('I', 'O'), igc.values()):
        cep = copy(ep)
        cep[ep_idx.ROW] = row
        cep[ep_idx.EP_TYPE] = not ep[ep_idx.EP_TYPE]
        cep[ep_idx.REFERENCED_BY] = []
        ret_val[hash_ep(cep)] = cep
    return ret_val


def _complete_references(igc):
    """Complete any incomplete references in igc.

    An incomplete reference is when a destination references
    a source but the source does not reference the destination.
    This is usually a side effect of insertion.
    igc is modified.

    Args
    ----
    igc (dict): Internal gc_graph format gc_graph.
    """
    for ep in filter(lambda x: x[ep_idx.EP_TYPE] == DST_EP and x[ep_idx.REFERENCED_BY], igc.values()):
        for ref in ep[ep_idx.REFERENCED_BY]:
            igc[hash_ref(ref, SRC_EP)][ep_idx.REFERENCED_BY].append(hash_ref(ref, DST_EP))


def _insert(igc_gcg, tgc_gcg, above_row):
    """Insert igc into the internal graph above row above_row.

    See https://docs.google.com/spreadsheets/d/1YQjrM91e5x30VUIRzipNYX3W7yiFlg6fy9wKbMTx1iY/edit?usp=sharing
    for more details (ask permission to view).
    graph is not modified.

    Args
    ----
    igc (gc_graph): Internal gc_graph format gc_graph to insert.
    tgc (gc_graph): Internal gc_graph format gc_graph to insert into.
    above_row (str): 'A', 'B' or 'O'

    Returns
    -------
    (gc_graph, gc_graph): rgc, fgc
    """
    tgc = tgc_gcg.graph
    igc = igc_gcg.graph
    rgc = _copy_clean_row(tgc, 'IC')
    fgc = {}
    if not tgc_gcg.has_a():
        _logger.debug("Case 1")
        rgc.update(_insert_as(igc, 'A'))
        rgc.update(_copy_row(tgc, 'O'))
    elif not tgc_gcg.has_b():
        if above_row == 'A':
            _logger.debug("Case 2")
            rgc.update(_insert_as(igc, 'A'))
            rgc.update(_move_row(tgc, 'A', None, 'B', None)) 
            rgc.update(_redirect_refs(_copy_row(tgc, 'O'), 'O', DST_EP, 'A', 'B'))
        else:
            _logger.debug("Case 3")
            rgc.update(_copy_row(tgc, 'A'))
            rgc.update(_insert_as(igc, 'B'))
            rgc.update(_copy_row(tgc, 'O'))
    else:
        if above_row == 'A':
            _logger.debug("Case 4")
            fgc.update(_copy_clean_row(tgc, 'IC'))
            fgc.update(_insert_as(igc, 'A'))
            fgc.update(_move_row(tgc, 'A', None, 'B', None))
            fgc.update(_direct_connect(fgc, 'B', 'O'))
            fgc.update(_append_connect(fgc, 'A', 'O'))
            rgc.update(_direct_connect(rgc, 'I', 'A'))
            rgc.update(_move_row(fgc, 'O', None, 'A', SRC_EP, True))
            rgc.update(_copy_row(tgc, 'B'))
            rgc.update(_copy_row(tgc, 'O'))
        elif above_row == 'B':
            _logger.debug("Case 5")
            fgc.update(_copy_clean_row(tgc, 'IC'))
            fgc.update(_copy_row(tgc, 'A'))
            fgc.update(_insert_as(igc, 'B'))
            fgc.update(_direct_connect(fgc, 'A', 'O'))
            fgc.update(_append_connect(fgc, 'B', 'O'))
            rgc.update(_direct_connect(rgc, 'I', 'A'))
            rgc_update(_move_row(fgc, 'O', None, 'A', SRC_EP, True))
            rgc.update(_copy_row(tgc, 'B'))
            rgc.update(_copy_row(tgc, 'O'))
        else:
            _logger.debug("Case 6")
            rgc.update(_direct_connect(rgc, 'I', 'A'))
            rgc.update(_move_row(tgc, 'O', DST_EP, 'A', SRC_EP, True))
            rgc.update(_insert_as(igc, 'B'))
            rgc.update(_direct_connect(rgc, 'A', 'O'))

    _logger.debug("rgc: {}".format(pformat(rgc)))
    _complete_references(rgc)
    rgc_graph = gc_graph()
    rgc_graph.graph = rgc
    if fgc:
        _logger.debug("fgc: {}".format(pformat(fgc)))
        _complete_references(fgc)
        fgc_graph = gc_graph()
        fgc_graph.graph = fgc
    else:
        fgc_graph = {}
    return rgc_graph, fgc_graph


def gc_insert(target_gc, insert_gc, above_row):
    """Insert insert_gc into target_gc above row 'above_row'.

    A work stack is used to avoid recursion.

    Insertion work is pushed onto the work_stack.
    While there is work to do:
        Pop work off the work stack.
        If the target_gc has a B row then to insert a GC will
        require two new ones to be made: One to combine the top two
        GC's and a second to bind that GC to the bottom one (fgc & tgc respectively).
        fgc is not restricted to have the same inputs and outputs as the
        target_gc unlike tgc which must. If either fgc or tgc is not
        in a steady state then a steady state exception is thrown the handler of
        which will return insertion work to complete the graph. That work will be
        added to the top of the work stack. Steady state GC's are added to the
        return value, fgc to the back and tgc to the front, thus when the function
        returns the correct tgc will be at the head of the fgc_list.

    Args
    ----
    target_gc (gc): GC to insert insert_gc into.
    insert_gc (gc): GC to insert into target_gc.
    above_row (string): One of 'A', 'B' or 'O'.

    Returns
    -------
    ([fgc]): List of fGC's. Element 0 may replace target_gc.
    Subsequent fGC's are children of element 0. 
    """
    work_stack = [(target_gc, insert_gc, above_row)]
    fgc_list = []
    while work_stack:
        _logger.debug("Work stack depth: {}".format(len(work_stack)))
        fgc = {}
        rgc = {}
        target_gc, insert_gc, above_row = work_stack.pop(0)
        _logger.debug("Work: Target={}, Insert={}, Above Row={}".format(target_gc['signature'], insert_gc['signature'], above_row))
        # TODO: Get rid of NULL_GC (make it None)

        # Insert into the graph
        tgc_graph = gc_graph(target_gc['graph'])
        igc_graph = gc_graph(insert_gc['graph'])
        rgc_graph, fgc_graph = _insert(igc_graph, tgc_graph, above_row)
        if fgc_graph:
            fgc_steady = fgc_graph.normalize()
            fgc['graph'] = fgc_graph.app_graph
            fgc['signature'] = define_signature(fgc)
        rgc_steady = rgc_graph.normalize()
        rgc['graph'] = rgc_graph.app_graph
        rgc['signature'] = define_signature(rgc)

        #Insert into the GC
        if not tgc_graph.has_a(): # Case 1
            _logger.debug("Case 1")
            rgc['gca'] = insert_gc['signature']
        elif not tgc_graph.has_b():
            if above_row == 'A': # Case 2
                _logger.debug("Case 2")
                rgc['gca'] = insert_gc['signature']
                rgc['gcb'] = target_gc['gca'] if target_gc['gca'] != NULL_GC else target_gc['signature'] # Consider codon case
            else: # Case 3
                _logger.debug("Case 3")
                rgc['gca'] = target_gc['gca'] if target_gc['gca'] != NULL_GC else target_gc['signature'] # Consider codon case
                rgc['gcb'] = insert_gc['signature']
        else: # Has row A & row B
            if above_row == 'A': # Case 4
                _logger.debug("Case 4")
                fgc['gca'] = insert_gc['signature']
                fgc['gcb'] = target_gc['gca']
                rgc['gca'] = fgc['signature']
                rgc['gcb'] = target_gc['gcb']
            elif above_row == 'B': # Case 5
                _logger.debug("Case 5")
                fgc['gca'] = insert_gc['signature']
                fgc['gcb'] = target_gc['gcb']
                rgc['gca'] = target_gc['gca']
                rgc['gcb'] = fgc['signature']
            else: # Case 6
                _logger.debug("Case 6")
                rgc['gca'] = target_gc['signature']
                rgc['gcb'] = insert_gc['signature']

        # Check we have valid graphs
        if fgc_graph:
            if not fgc_steady:
                work_stack.insert(0, steady_state_exception(fgc))
            else:
                fgc_list.append(fgc)

        if not rgc_steady:
            work_stack.insert(0, steady_state_exception(rgc))
        else:
            fgc_list.insert(0, rgc)

    _logger.debug("fgc_list: {}".format(pformat(fgc_list)))
    return fgc_list


def steady_state_exception(fgc):
    """Define what GC must be inserted to complete or partially complete the fgc graph.

    fgc is analysed to determine what end point destinations are unconnected and the highest row
    on which one or more of the unconnected destination endpoints resides.

    Candidate GC's to plug the gap are found using the following criteria:
        1. All input types required by the candidates are available at the row it is to be inserted
        2. All unconnected endpoint types are output types of the candidates

    If there are multiple valid candidates one is randomly returned.

    In the event there are no matches an attempt is made to reduce the delta by finding candidate GC's where:
        1. All input types required by the candidates are available at the row it is to be inserted
        2. A subset of unconnected endpoint types are output types of the candidates

    If there are multiple valid candidates one is randomly returned.

    In the event there are no matches again it is not possible to guarantee a reduction in the delta.
    GC candidates are sought that alter the problem space:
        1. A subset of types required by the candidates are available at the row it is to be inserted
        2. A subset of unconnected endpoint types are output types of the candidates

    If there are multiple valid candidates one is randomly returned. If a candidate cannot be found
    then there exists no direct route from any of the available inputs types to any one of the required
    output types.

    Finally, GC candidates are sought where:
        1. A subset of unconnected endpoint types are output types of the candidates
        2. No unconnected endpoint types are input types of the candidates
    These candidates effectively do a type conversion to change the problem space for a subset of the
    unconnected enpoints.

    If there are multiple valid candidates one is randomly returned. If a candidate cannot be found then
    there is no way to connect the unconnected destination endpoints and an exception it thrown.

    Args
    ----
    fgc (fGC): fGC with incomplete graph.

    Returns
    -------
    (fGC, fGC, str): target_gc, insert_gc, 'A', 'B' or 'O'.
    """
    fgc_graph = gc_graph(fgc['graph'])

    # Find unconnected destination endpoints. Determine highest row & endpoint types. 
    dst_list = list(filter(fgc_graph.unreferenced_filter(fgc_graph.dst_filter()), fgc_graph.graph.values()))
    above_row = 'Z'
    output_types = set()
    for ep in dst_list:
        if ep[ep_idx.ROW] < above_row: above_row = ep[ep_idx.ROW]
        output_types.add(ep[ep_idx.TYPE])
    output_types = list(output_types)

    # Find viable source types above the highest row.
    src_list = list(filter(fgc_graph.rows_filter(fgc_graph.src_rows[above_row], fgc_graph.src_filter()), fgc_graph.graph.values()))
    input_types = list(set([ep[ep_idx.TYPE] for ep in src_list]))

    # TODO: Do we select random or by evolvability?
    # Create microbiome query & return if we find a match
    query = {
        "input_types": {
            "operator": "contained by",
            "array": input_types
        },
        "output_types": {
            "operator": "contains",
            "array": output_types
        },
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # No viable candidates - look to reduce the delta
    # Create microbiome query & return if we find a match
    query = {
        "input_types": {
            "operator": "contained by",
            "array": input_types
        },
        "output_types": {
            "operator": "overlaps",
            "array": output_types
        },
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # No viable candidates - look to reduce the delta
    # Create microbiome query & return if we find a match
    query = {
        "input_types": {
            "operator": "overlaps",
            "array": input_types
        },
        "output_types": {
            "operator": "overlaps",
            "array": output_types
        },
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # No viable candidates - look to reduce the delta
    # Create microbiome query & return if we find a match
    query = {
        "input_types": {
            "operator": "does not overlap",
            "array": input_types
        },
        "output_types": {
            "operator": "overlaps",
            "array": output_types
        },
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # !
    raise wtf
