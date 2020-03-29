'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/definition.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, March 29th 2020, 3:35:10 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from datetime import datetime
from hashlib import sha256


# Cerberus "default_setter" functions


NULL_GC = "0" * 64


def set_signature(document):

    # The signature for a codon GC is slightly different
    string = str(document["graph"]["A"]) + str(document["graph"]["O"])
    string += document["GCA"] + document["GCB"]
    if "B" in document["graph"]: string += str(document["graph"]["B"])
    if "C" in document["graph"]: string += str(document["graph"]["C"])

    # If it is a codon glue on the mandatory definition
    if document["GCA"] == NULL_GC:
        string += document["meta_data"]["function"]["python3"]["0"]["inline"]
        string += document["meta_data"]["function"]["python3"]["0"]["callable"]

    # Remove spaces etc. to give some degrees of freedom in formatting and
    # not breaking the signature
    return sha256("".join(string.split()).encode()).hexdigest()


def set_num_inputs(document):
    i_indices = set()
    for pr in document["graph"].values():
        for r, i in pr:
            if r == "I": i_indices.add(i)
    return len(i_indices)


def set_num_outputs(document):
    return len(document["graph"]["O"])


def set_created(document):
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
