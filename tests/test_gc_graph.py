"""gc_graph verficiation."""


import pytest
from os.path import dirname, join
from json import load
from random import choice, randint
from microbiome.genetics.gc_graph import gc_graph, conn_idx, const_idx, DST_EP, SRC_EP, DESTINATION_ROWS, SOURCE_ROWS
from microbiome.genetics.gc_type import asint
from logging import getLogger, basicConfig, DEBUG, INFO


basicConfig(filename='erasmus.log', level=INFO)
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


with open(join(dirname(__file__), _TEST_RESULTS_JSON), "r") as results_file: results = load(results_file)


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
    graph = gc_graph()
    structure = choice(_VALID_STRUCTURES)
    for row in structure:
        graph.app_graph[row] = []
        if not row in ('U', 'P'):
            if row in DESTINATION_ROWS and any([src_row in structure for src_row in gc_graph.src_rows[row]]):
                count = 1 if row == 'F' else randint(1, 10)
                for i in range(count): graph.graph[graph.hash_ref([row, i], DST_EP)] = [DST_EP, row, i, 'int', []]
                if row == 'O' and 'P' in structure:
                    for i in range(count): graph.graph[graph.hash_ref(['P', i], DST_EP)] = [DST_EP, 'P', i, 'int', []]

            if row in SOURCE_ROWS:
                for i in range(randint(1, 8)):
                    ep = [SRC_EP, row, i, 'int', []]
                    if row == 'C': ep.append(randint(-1000, 1000))
                    graph.graph[graph.hash_ref([row, i], SRC_EP)] = ep

    for _ in range(len(list(filter(graph.dst_filter(), graph.graph.values())))): graph.random_add_connection()
    graph.normalize()
    assert graph.validate()

    #TODO: Split this out into its own test case when the graphs are staticly defined in a JSON file.
    for _ in range(int(len(list(filter(graph.dst_filter(), graph.graph.values()))) / 2)): graph.random_remove_connection()
    for _ in range(len(list(filter(graph.dst_filter(), graph.graph.values())))): graph.random_add_connection()
    graph.normalize()
    assert graph.validate()
    #graph.draw('graph_' + str(test))


