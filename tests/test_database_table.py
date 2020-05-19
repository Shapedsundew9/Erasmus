'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_database_table.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Saturday, April 25th 2020, 6:10:10 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


import pytest
from os.path import join, dirname
from json import load
from microbiome.query_validator import query_validator
from microbiome.config import set_config, get_config
from microbiome.database_table import database_table
from logging import getLogger, basicConfig, DEBUG


test_config = load(open(join(dirname(__file__), "test_config.json"), "r"))
queries = load(open(join(dirname(__file__), "test_entry_queries.json"), "r"))
results = load(open(join(dirname(__file__), "test_entry_results.json"), "r"))
schema = load(open(join(dirname(__file__), "test_entry_format.json"), "r"))
basicConfig(filename='erasmus.log', level=DEBUG)


@pytest.fixture(scope="module")
def test_table():
    data = load(open(join(dirname(__file__), "test_entry_data.json"), "r"))
    set_config(test_config)
    table = database_table(getLogger(__file__), "test_table", "test_database")
    table.store(data)
    return table


@pytest.mark.parametrize("index", list(range(len(queries))))
def test_db_load(index, test_table):
    query = queries[index]
    result = results[index]
    assert test_table.load(query) == result


def test_history_decimation():
    set_config(test_config)
    table = database_table(getLogger(__file__), "test_history_decimation", "test_database")
    hd_config = get_config()['databases']['test_database']['tables']['test_history_decimation']['history_decimation']
    assert hd_config['phase_size'] == 4
    assert hd_config['num_phases'] == 4

    # Fill the first phase and ensure all the idxs are there.
    table.store([{'id': 'test 1'}] * (1 << hd_config['phase_size']))
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    for r, idx in zip(table.load([{'order by': 'idx'}]), expected): assert r['idx'] == idx

    # Add 2 more entries.
    # The entry with idx == 1 should have been deleted because it overflowed the first phase/stack and
    # does not meet the selection criteria for the second phase/stack
    table.store([{'id': 'test 2'}] * 2)
    expected = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    for r, idx in zip(table.load([{'order by': 'idx'}]), expected): assert r['idx'] == idx

    # Fill the whole table
    expected = [  8,  16,  24,  32,  40,  48,  56,  64,  72,  80,  88,  96, 104, 112, 120, 128,
                136, 140, 144, 148, 152, 156, 160, 164, 168, 172, 176, 180, 184, 188, 192, 196,
                200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230,
                231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246 
    ]
    table.store([{'id': 'test 3'}] * 228)
    # for r in table.load([{'order by': 'idx'}]): print(r)
    for r, idx in zip(table.load([{'order by': 'idx'}]), expected): assert r['idx'] == idx

    # Overflow the table with 15 more samples
    expected = [  24,  32,  40,  48,  56,  64,  72,  80,  88,  96, 104, 112, 120, 128, 136, 144,
                 152, 156, 160, 164, 168, 172, 176, 180, 184, 188, 192, 196, 200, 204, 208, 212,
                 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244,
                 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261 
    ]
    table.store([{'id': 'test 4'}] * 15)
    #for r in table.load([{'order by': 'idx'}]): print(r['idx'], ", ", end="")
    for r, idx in zip(table.load([{'order by': 'idx'}]), expected): assert r['idx'] == idx


