

import pytest
from os import linesep
from os.path import dirname, join
from tqdm import tqdm
from json import load, dumps
from microbiome.genetics.gc_type import __ALL_FLOATS, __ALL_OBJECTS, __ALL_SIGNED_INTEGERS, __ALL_UNSIGNED_INTEGERS
from microbiome.genetics.gc_type import *


__TEST_RESULTS_JSON = 'test_gc_type_results.json'
test_cases = []
for r in (__ALL_FLOATS, __ALL_OBJECTS, __ALL_SIGNED_INTEGERS, __ALL_UNSIGNED_INTEGERS):
    test_cases.extend(list(r))


def __write_results():
    """ Utility function to write out the expected results for every possible type.

    The resulting JSON file MUST be manually inspected to ensure it is correct.
    """
    results = []
    for i in tqdm(test_cases):
        if validate(i):
            results.append([
                i, 
                hex(asint(i)),
                asstr(i),
                asdict(i),
                is_int(i),
                is_unsigned(i),
                is_fp(i),
                is_numeric(i),
                is_object(i),
                is_template(i),
                is_reserved_obj(i),
                is_user_obj(i)
            ])
        else:
            results.append(last_validation_error())

    with open(join(dirname(__file__), __TEST_RESULTS_JSON), "w") as f1:
        f1.write('[' + linesep)
        for r in results[:-1]:
            f1.write('\t' + dumps(r) + ',' + linesep)
        f1.write('\t' + dumps(results[-1]) + linesep + ']'+ linesep)


#__write_results()


with open(join(dirname(__file__), __TEST_RESULTS_JSON), "r") as results_file: results = load(results_file)
@pytest.mark.parametrize("case", results)
def test_all_types(case):
    i = case[0]
    expected = str(last_validation_error()) if not validate(i) else str([
        i,
        hex(asint(i)),
        asstr(i),
        asdict(i),
        is_int(i),
        is_unsigned(i),
        is_fp(i),
        is_numeric(i),
        is_object(i),
        is_template(i),
        is_reserved_obj(i),
        is_user_obj(i)
    ])
    assert str(case) == expected



@pytest.mark.parametrize("value", test_cases)
def test_conversions(value):
    if validate(value): 
        value_as_dict = asdict(value)
        value_as_str = asstr(value)
        assert str(value) == str(asint(value_as_dict))
        assert value_as_str == asstr(asint(value_as_str))