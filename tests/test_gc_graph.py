"""gc_graph verficiation."""


import pytest
from os.path import join, dirname, basename, splitext
from json import load
from random import choice, randint, random
from numpy.random import choice
from microbiome.genetics.gc_graph import gc_graph, conn_idx, const_idx, DST_EP, SRC_EP, DESTINATION_ROWS, SOURCE_ROWS
from microbiome.genetics.gc_type import asint
from logging import getLogger, basicConfig, DEBUG, INFO


_TEST_RESULTS_JSON = 'data/test_gc_graph_results.json'
_VALID_STRUCTURES = (
        ('A', 'O'),
        ('C', 'O'),
        ('I', 'O'),
        ('A', 'O', 'U'),
        ('C', 'O', 'U'),
        ('I', 'O', 'U'),
        ('A', 'C', 'O'),
        ('A', 'I', 'O'),
        ('A', 'B', 'O'),
        ('I', 'C', 'O'),
        ('A', 'C', 'O', 'U'),
        ('A', 'I', 'O', 'U'),
        ('A', 'B', 'O', 'U'),
        ('I', 'C', 'O', 'U'),
        ('A', 'C', 'O', 'B'),
        ('A', 'I', 'O', 'B'),
        ('I', 'O', 'F', 'P'),
        ('A', 'C', 'O', 'B', 'U'),
        ('A', 'I', 'O', 'B', 'U'),
        ('I', 'O', 'F', 'P', 'U'),
        ('A', 'I', 'O', 'F', 'P'),
        ('I', 'C', 'O', 'F', 'P'),
        ('A', 'I', 'O', 'F', 'P', 'U'),
        ('I', 'C', 'O', 'F', 'P', 'U'),
        ('A', 'I', 'O', 'B', 'F', 'P'),
        ('A', 'I', 'O', 'B', 'F', 'P', 'U')
    )


with open(join(dirname(__file__), _TEST_RESULTS_JSON), "r") as results_file:
    results = load(results_file)


basicConfig(
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)
logger = getLogger(__file__)


def random_type(p=0.0):
    if random() < p: return choice(('obj131', 'int', 'float', 'bool', 'str'))
    return 'int'


def random_graph(p=0.0):
    """Create a random graph.

    The graph is not guaranteed to be valid when p > 0.0. If a destination row requires a type that
    is not present in any valid source row the graph cannot be normalized.

    Args
    ----
    p (float): 0.0 <= p <= 1.0 probability of choosing a random type on each type selection.

    Returns
    -------
    graph 
    """
    graph = gc_graph()
    structure = choice(_VALID_STRUCTURES)
    valid = False
    while not valid:
        destinations = {row: randint(1, 10) for row in structure if row in DESTINATION_ROWS and not row in ('F', 'U', 'P')}
        if 'F' in structure: destinations['F'] = 1
        sources = {row: randint(1, 8) for row in structure if row in SOURCE_ROWS and not row in ('U', 'P')}
        destination_types = [random_type(p) for row in destinations.values() for _ in range(row)]
        type_set = set(destination_types)
        valid = sum(sources.values()) >= len(type_set)
        logger.info("Invalid random configuration for structrue {}. Retrying...".format(structure))
    source_types = [random_type(p) for _ in range(sum(sources.values()))]
    indices = choice(sum(sources.values()), len(type_set), replace=False)
    for idx in indices: 
        source_types[idx] = type_set.pop()
    for _ in range(len(type_set)):
        source_types[randint(len(source_types))] = type_set

    for row in structure:
        graph.app_graph[row] = []
        if not row in ('U', 'P'):
            if row in DESTINATION_ROWS and any([src_row in structure for src_row in gc_graph.src_rows[row]]):
                for i in range(destinations[row]):
                    rtype = destination_types.pop()
                    graph.graph[graph.hash_ref([row, i], DST_EP)] = [DST_EP, row, i, rtype, []]
                    if row == 'O' and 'P' in structure:
                        graph.graph[graph.hash_ref(['P', i], DST_EP)] = [DST_EP, 'P', i, rtype, []]

            if row in SOURCE_ROWS:
                for i in range(sources[row]):
                    ep = [SRC_EP, row, i, source_types.pop(), []]
                    if row == 'C': ep.append(ep[3] + '(' + str(randint(-1000, 1000)) + ')')
                    graph.graph[graph.hash_ref([row, i], SRC_EP)] = ep

    for _ in range(len(list(filter(graph.dst_filter(), graph.graph.values())))): graph.random_add_connection()
    graph.normalize()
    return graph


@pytest.mark.good
@pytest.mark.parametrize("i, case", enumerate(results))
def test_graph_validation(i, case):
    """Verification the validate() method correctly functions."""
    gcg = gc_graph(case['graph'])
    assert i == case['i']
    assert case['valid'] == gcg.validate()
    if not case['valid']: assert all([e in [g.code for g in gcg.status] for e in case['errors']])


@pytest.mark.good
@pytest.mark.parametrize("i, case", enumerate(results))
def test_graph_conversion(i, case):
    """Verification that converting to internal format and back again is the identity operation."""
    gcg = gc_graph(case['graph'])
    assert i == case['i']
    if case['valid']:
        for k, v in case['graph'].items():
            idx = const_idx.TYPE if k == 'C' else conn_idx.TYPE
            for r in v: r[idx] = asint(r[idx])   
        assert case['graph'] == gcg.application_graph()


@pytest.mark.good
@pytest.mark.parametrize("test", range(100))
def test_add_connection_simple(test):
    """Verify adding connections makes valid graphs.
    
    Create a random graph with unconnected source and destination endpoints
    then connect them together using the random_add_connection() method
    of gc_graph. To keep it simple all the endpoints have the same type ("int"). 
    """
    # TODO: These random test cases need to be made static when we are confident in them.
    # Generate them into a JSON file.
    graph = random_graph()
    assert graph.validate()

    #TODO: Split this out into its own test case when the graphs are staticly defined in a JSON file.
    for _ in range(int(len(list(filter(graph.dst_filter(), graph.graph.values()))) / 2)): graph.random_remove_connection()
    graph.normalize()
    assert graph.validate()
    #graph.draw('graph_' + str(test))


@pytest.mark.good
@pytest.mark.parametrize("test", range(100))
def test_add_connection(test):
    """Verify adding connections makes valid graphs.
    
    In this version multiple types endpoint types are used. This can lead to a legitimate invalid
    graph with error codes E01001 or E01004.
    """
    # TODO: These random test cases need to be made static when we are confident in them.
    # Generate them into a JSON file.
    gc = random_graph(0.5)
    if not gc.validate():
        codes = set([t.code for t in gc.status])
        codes.discard('E01001')
        codes.discard('E01004')
        assert not codes

