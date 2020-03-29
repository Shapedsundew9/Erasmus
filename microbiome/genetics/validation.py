'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/validation.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, March 29th 2020, 2:20:33 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from cerberus import Validator
from datetime import datetime
from os.path import isfile
from json import load
from .definition import *


ENTRY_VALIDATION_FILE = "./microbiome/genetics/entry_format.json"


def valid_graph(field, value, error):

    # If "B" does not exist there must be no references to it.
    if not "B" in value:
        for r, i in value["O"]:
            if r == "B": error(field, "B referenced from O but does not exist: [{},{}]".format(r, i))

    # If "C" does not exist there must be no references to it.
    if not "C" in value:
        for pr in value.values():
            for r, i in pr:
                if r == "C": error(field, "C referenced from {} but does not exist: [{},{}]".format(pr, r, i))

    # If C does exist index references must be in range
    if "C" in value:
        c_len = len(value["c"])
        for pr in value.values():
            if pr != "C":
                for r, i in pr:
                    if r == "C" and i >= c_len:
                         error(field, "Reference into C from {} out of bounds. Max index = {}: [{},{}]".format(pr, c_len, r, i))

    # All values in "C" must be referenced at least once
    if "C" in value:
        c_indices = set()
        for pr in value.values():
            for r, i in pr:
                if r == "C": c_indices.add(i)
        c_indices = list(c_indices)
        if sorted(c_indices) != range(len(c_indices)): error(field, "Missing at least one reference to C")

    # References to I must start at 0 and be contiguous
    i_indices = set()
    for pr in value.values():
        for r, i in pr:
            if r == "I": i_indices.add(i)
    i_indices = list(i_indices)
    if sorted(i_indices) != list(range(len(i_indices))): error(field, "Missing at least one reference to I")


def valid_created(field, value, error):
    try:
        date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        error(field, "Created date-time is not valid. Unknown error parsing.")
        return

    if date_time_obj > datetime.now():
        error(field, "Created date-time cannot be in the future.")


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


def create_validator():
    if not isfile(ENTRY_VALIDATION_FILE): assert False, "Cannot find {}".format(ENTRY_VALIDATION_FILE)
    with open(ENTRY_VALIDATION_FILE, "r") as file_ptr: schema = set_callables(load(file_ptr))
    return Validator(schema)
