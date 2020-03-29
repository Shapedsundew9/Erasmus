'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/validation.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, March 29th 2020, 2:20:33 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from datetime import datetime


# Cerberus "check_with" validation functions.


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

