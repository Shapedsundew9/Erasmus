"""Test query generation."""

import pytest
from os.path import join, dirname, splitext, basename
from json import load
from microbiome.query_validator import query_validator
from microbiome.entry_column_meta_validator import entry_column_meta_validator
from logging import getLogger, basicConfig, DEBUG


# Load test files
with open(join(dirname(__file__), "data/test_entry_queries.json"), "r") as fileptr:
    queries = load(fileptr)
with open(join(dirname(__file__), "data/test_entry_format.json"), "r") as fileptr:
    schema = load(fileptr)
for k, v in schema.items(): v['meta'] = entry_column_meta_validator.normalized(v['meta'])


basicConfig(
    filename=join(
        dirname(__file__),
        'logs',
        splitext(basename(__file__))[0] + '.log'),
    filemode='w',
    level=DEBUG)


@pytest.mark.good
def test_query_validator_init():
    """Construction validation."""
    validator = query_validator(schema, "test")
    validator.create_query_format_json()


@pytest.mark.good
@pytest.mark.parametrize("query", queries)
def test_query_validation(query):
    """Validate a set of queries."""
    validator = query_validator(schema, "test")
    assert validator.validate(query), str(validator.errors)




