"""The operation that can be performed on a GC dictionary."""
from .genomic_library_entry_validator import NULL_GC
from gc_graph import gc_graph, ep_idx
from random import getrandbits
from copy import deepcopy, copy


NULL_GC_TYPE = 0
INPUT_LHS = ["input0_type", "input1_type", "input2_type", "input3_type", "input4_type", "input5_type", "input6_type", "input7_type"]
OUTPUT_LHS = ["output0_type", "output1_type", "output2_type", "output3_type"]
INPUT_DICT = {"lhs": INPUT_LHS, "rhs": None}
OUTPUT_DICT = {"lhs": OUTPUT_LHS, "rhs": None}


def gc_insert(target_gc, insert_gc, above_row):
    """Insert insert_gc into target_gc above row 'above_row'.

    A work stack is used to avoid recursion.

    Insertion work is pushed onto the work_stack.
    While there is work to do:
        Pop work off the work stack.
        If the target_gc has a B row then to insert a GC will
        require two new ones to be made: One to combine the top two
        GC's and a second to bind that GC to the bottom one (fgc & tgc respectively).
        The insert_gc will be slotted according to above_row.
            #1 Target has row B & above_row = 'A': tgc = {
                gca = { gca = insert_gc, gcb = target.gca }
                gcb = target.gcb
            }
            #2 Target has row B & above_row = 'B': tgc = {
                gca = { gca = target.gca, gcb = insert_gc }
                gcb = target.gcb
            }
            #3 Target has row B & above_row = 'O': tgc = {
                gca = { gca = target.gca, gcb = target.gcb }
                gcb = insert_gc
            }
            #4 Target does not have row B & above_row = 'A': tgc = {
                gca = insert_gc
                gcb = target.gca
            }
            #5 Target does not have row B & above_row = 'B': tgc = {
                gca = target.gca
                gcb = insert_gc
            }
            #6 Target does not have row B & above_row = 'O': tgc = {
                gca = target.gca
                gcb = insert_gc
            }
        fgc is not restricted to have the same inputs and outputs as the
        target_gc unlike tgc which must. If either fgc or tgc is not
        in a steady state then a steady state exception is thrown the handler of
        which will return insertion work to complete the graph. That work will be
        added to the from of the work stack. Steady state GC's are added to the
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
        fgc = {}
        target_gc, insert_gc, above_row = work_stack.pop(0)
        target_has_b = target_gc['gcb'] != NULL_GC
        target_graph = gc_graph(target_gc['graph'])
        fgc_graph = deepcopy(target_graph)
        if target_has_b:
            if above_row == 'A':
                fgc['gca'] = insert_gc['signature']
                fgc['gcb'] = target_gc['gca']
                fgc_graph.insert(insert_gc, above_row)
            if above_row == 'B':
                fgc['gca'] = target_gc['gca']
                fgc['gcb'] = insert_gc['signature']
                fgc_graph.insert(insert_gc, above_row)
            if above_row == 'O':
                fgc['gca'] = target_gc['gca']
                fgc['gcb'] = target_gc['gcb']
            fgc['signature'] = hex(getrandbits(256))[2:]
            steady = fgc_graph.normalise(True)
            fgc['graph'] = fgc_graph.app_graph
            if not steady:
                work_stack.insert(0, steady_state_exception(fgc, delta))
            else:
                fgc_list.append(fgc)

        tgc = {}
        if target_has_b:
            tgc['gca'] = fgc['signature']
            tgc['gcb'] = target_gc['gcb'] if above_row != 'O' else insert_gc['signature']
        else:
            if above_row == 'A':
                tgc['gca'] = insert_gc['signature']
                tgc['gcb'] = target_gc['gca']
                tgc_graph.insert(insert_gc, above_row)
            if above_row in ('B', 'O'):
                tgc['gca'] = target_gc['gca']
                tgc['gcb'] = insert_gc['signature']
                tgc_graph.insert(insert_gc, above_row)
        tgc['signature'] = hex(getrandbits(256))[2:]
        steady = target_graph.normalise()
            tgc['graph'] = target_graph.app_graph
        if not steady:
            work_stack.insert(0, steady_state_exception(tgc))
        else:
            fgc_list.insert(0, tgc)

        return fgc_list


def steady_state_exception(fgc)
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
    OUTPUT_DICT['rhs'] = list(output_types)

    # Find viable source types above the highest row.
    src_list = list(filter(fgc_graph.rows_filter(fgc_graph.src_rows[above_row], fgc_graph.src_filter()), fgc_graph.graph.values()))
    input_types = list(set([ep[ep_idx.TYPE] for ep in src_list]))
    input_types_plus = copy(input_types)
    input_types_plus.append(NULL_GC_TYPE)
    INPUT_DICT['rhs'] = input_types

    # Create microbiome query & return if we find a match
    query = {
        "contained by": {
            "lhs": INPUT_LHS,
            "rhs": input_types_plus
        },
        "contains": OUTPUT_DICT,
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # No viable candidates - look to reduce the delta
    # Create microbiome query & return if we find a match
    query = {
        "contained by": INPUT_DICT,
        "overlaps": OUTPUT_DICT,
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # No viable candidates - look to reduce the delta
    # Create microbiome query & return if we find a match
    query = {
        "overlaps": INPUT_DICT,
        "overlaps": OUTPUT_DICT,
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # No viable candidates - look to reduce the delta
    # Create microbiome query & return if we find a match
    query = {
        "does not overlap": {
            "lhs": INPUT_LHS,
            "rhs": OUTPUT_DICT['rhs']
        },
        "overlaps": OUTPUT_DICT,
        "order by": "RANDOM()",
        "limit": 1
    }
    results = gl.load(query, ('signature', 'gca', 'gcb', 'graph'))
    if results: return (fgc, results[0], above_row)

    # !
    raise wtf
