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

    # Fill the first phase and ensure all the idxs are there.
    table.store([{'id': 'test 1'}] * (1 << hd_config['phase_size']))
    expected = list(range(1, (1 << hd_config['phase_size']) + 1))
    for r, idx in zip(table.load([{'order by': 'idx'}]), expected): assert r['idx'] == idx

    # Add 2 more entries.
    # The second entry (of the originals i.e. entry idx = 2) should not be stored
    table.store([{'id': 'test 2'}] * 2)
    expected = list(range(1, (1 << hd_config['phase_size']) + 3))
    expected.remove(1)
    for r, idx in zip(table.load([{'order by': 'idx'}]), expected): assert r['idx'] == idx

    # Fill the whole table
    expected = [  0,   8,  16,  24,  32,  40,  48,  56,  64,  72,  80,  88,  96, 104, 112, 120,
                124, 128, 132, 136, 140, 144, 148, 152, 156, 160, 164, 168, 172, 176, 180, 184,
                186, 188, 190, 192, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216,
                217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232
    ]
    table.store([{'id': 'test 3'}] * 228)
    print(table.load([{'order by': 'idx'}]))
    exit(1)
    list(range(1 << hd_config['phase_size'] + 1))
    expected.extend(list(range(1, 1 << (hd_config['phase_size'] + 1))))
    for r, idx in zip(table.load([{'order by': 'idx'}]), expected): assert r['idx'] == idx


