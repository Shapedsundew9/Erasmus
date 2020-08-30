

import pytest
from os.path import dirname, join
from json import load
from microbiome.genetics.gc_graph_tools import gc_graph
from logging import getLogger, basicConfig, DEBUG


basicConfig(filename='erasmus.log', level=DEBUG)
__TEST_RESULTS_JSON = 'test_gc_graph_results.json'

with open(join(dirname(__file__), __TEST_RESULTS_JSON), "r") as results_file: results = load(results_file)
@pytest.mark.parametrize("i, case", enumerate(results))
def test_graphs(i, case):
    gcg = gc_graph(case['graph'])
    assert case['valid'] == gcg.validate()

    if not case['valid']: assert all([e in [g.code for g in gcg.errors] for e in case['errors']])
