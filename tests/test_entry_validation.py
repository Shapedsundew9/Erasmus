from json import load
from os.path import isfile
from cerberus import Validator
from microbiome.genetics.validation import *
from microbiome.genetics.definition import *


CODON_LIBRARY_FILE = "./microbiome/genetics/codon_library.json"
ENTRY_VALIDATION_FILE = "./microbiome/genetics/entry_format.json"


# Cerberus "check_with" and "default_setter" entries options require callable values
# The names of the functions are specified as strings in the JSON schema.
# The set_callables function recursively traverses the validation schema to find
# these fields and replace the string with the function object defined in
# either microbiome.genetics.validation or microbiome.genetics.definition 
def set_callables(schema):
    if "default_setter" in schema: schema["default_setter"] = eval(schema["default_setter"])
    if "check_with" in schema: schema["check_with"] = eval(schema["check_with"])
    for k, v in schema.items():
        if isinstance(v, dict): schema[k] = set_callables(v)
    return schema


def test_codon_library():
    if not isfile(CODON_LIBRARY_FILE): assert(False, "Cannot find {}".format(CODON_LIBRARY_FILE))
    if not isfile(ENTRY_VALIDATION_FILE): assert(False, "Cannot find {}".format(ENTRY_VALIDATION_FILE))
    with open(CODON_LIBRARY_FILE, "r") as file_ptr: codon_library = load(file_ptr)
    with open(ENTRY_VALIDATION_FILE, "r") as file_ptr: schema = set_callables(load(file_ptr))

    validator = Validator(schema)

    for codon in codon_library: assert validator(codon), codon["meta_data"]["name"] + ":" + str(validator.errors)

        