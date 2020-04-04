'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/validation.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, March 29th 2020, 2:20:33 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from cerberus import Validator
from datetime import datetime
from os.path import dirname, join
from json import load
from datetime import datetime
from hashlib import sha256


_NULL_GC = "0" * 64
_ENTRY_VALIDATION_SCHEMA = load(open(join(dirname(__file__), "entry_format.json"), "r"))


class entry_validator(Validator):

    _loaded = False

    # Hack to allow recursive object creation
    def __init__(self, *args, **kwargs):
        if entry_validator._loaded:
            super().__init__(args, kwargs)
        else:
            super().__init__(_ENTRY_VALIDATION_SCHEMA)
            entry_validator._loaded = True


    # TODO: Make errors ValidationError types for full disclosure
    # https://docs.python-cerberus.org/en/stable/customize.html#validator-error

    def _check_with_valid_graph(self, field, value):
        # If "B" does not exist there must be no references to it.
        if not "B" in value:
            for r, i in value["O"]:
                if r == "B": self._error(field, "B referenced from O but does not exist: [{},{}]".format(r, i))

        # If "C" does not exist there must be no references to it.
        if not "C" in value:
            for pr in value.values():
                for r, i in pr:
                    if r == "C": self._error(field, "C referenced from {} but does not exist: [{},{}]".format(pr, r, i))

        # If C does exist index references must be in range
        if "C" in value:
            c_len = len(value["c"])
            for pr in value.values():
                if pr != "C":
                    for r, i in pr:
                        if r == "C" and i >= c_len:
                            self._error(field, "Reference into C from {} out of bounds. Max index = {}: [{},{}]".format(pr, c_len, r, i))

        # All values in "C" must be referenced at least once
        if "C" in value:
            c_indices = set()
            for pr in value.values():
                for r, i in pr:
                    if r == "C": c_indices.add(i)
            c_indices = list(c_indices)
            if sorted(c_indices) != range(len(c_indices)): self._error(field, "Missing at least one reference to C")

        # References to I must start at 0 and be contiguous
        i_indices = set()
        for pr in value.values():
            for r, i in pr:
                if r == "I": i_indices.add(i)
        i_indices = list(i_indices)
        if sorted(i_indices) != list(range(len(i_indices))): self._error(field, "Missing at least one reference to I")


    # Checks for a valid codon or non-codon
    def _check_with_valid_alpha_class(self, field, value):

        if not value:
            # Valid codon
            if "beta_class" in self.document and self.document['beta_class']: self._error(field, "If alpha_class == 0, beta_class must == 0.")
            if "generation" in self.document and self.document['generation']: self._error(field, "If alpha_class == 0, generation must == 0.")
            if "codon_depth" in self.document and self.document['codon_depth'] != 1: self._error(field, "If alpha_class == 0, codon_depth must == 1.")
            if "code_depth" in self.document and self.document['code_depth'] != 1: self._error(field, "If alpha_class == 0, code_depth must == 1.")
            if "GCA" in self.document and self.document['GCA'] != _NULL_GC: self._error(field, "If alpha_class == 0, GCA must == " + _NULL_GC)
            if "GCB" in self.document and self.document['GCB'] != _NULL_GC: self._error(field, "If alpha_class == 0, GCB must == " + _NULL_GC)
            if "num_codes" in self.document and self.document['num_codes'] != 1: self._error(field, "If alpha_class == 0, num_codes must == 1.")
            if "raw_num_codons" in self.document and self.document['raw_num_codons'] != 1: self._error(field, "If alpha_class == 0, raw_num_codons must == 1.")
            if "opt_num_codons" in self.document and self.document['opt_num_codons'] != 1: self._error(field, "If alpha_class == 0, opt_num_codons must == 1.")
            if "meta_data" in self.document and "parents" in self.document['meta_data']: self._error(field, "If alpha_class == 0 then there are no parents.")
            if "meta_data" in self.document and not "function" in self.document['meta_data']:
                self._error(field, "If alpha_class == 0 then there must be a 'function' definition.")
            elif not "python3" in self.document['meta_data']['function']:
                self._error(field, "If alpha_class == 0 then there must be a 'python3' definition.")
        else:
            # Valid non-codon
            if "beta_class" in self.document and not self.document['beta_class']:  self._error(field, "If alpha_class != 0, beta_class must != 0.")
            if "generation" in self.document and not self.document['generation']: self._error(field, "If alpha_class != 0, generation must != 0.")
            if "GCA" in self.document and self.document['GCA'] == _NULL_GC: self._error(field, "If alpha_class != 0, GCA must != " + _NULL_GC)
            if "meta_data" in self.document and not "parents" in self.document['meta_data']: self._error(field, "If alpha_class != 0 then there mus be at least one parent.")


    def _check_with_valid_created(self, field, value):
        try:
            date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            self._error(field, "Created date-time is not valid. Unknown error parsing.")
            return

        if date_time_obj > datetime.now():
            self._error(field, "Created date-time cannot be in the future.")


    def _normalize_default_setter_set_signature(self, document):

        # The signature for a codon GC is slightly different
        string = str(document["graph"]["A"]) + str(document["graph"]["O"])
        string += document["GCA"] + document["GCB"]
        if "B" in document["graph"]: string += str(document["graph"]["B"])
        if "C" in document["graph"]: string += str(document["graph"]["C"])

        # If it is a codon glue on the mandatory definition
        if document["GCA"] == _NULL_GC:
            string += document["meta_data"]["function"]["python3"]["0"]["inline"]
            string += document["meta_data"]["function"]["python3"]["0"]["callable"]

        # Remove spaces etc. to give some degrees of freedom in formatting and
        # not breaking the signature
        return sha256("".join(string.split()).encode()).hexdigest()


    def _normalize_default_setter_set_num_inputs(self, document):
        i_indices = set()
        for pr in document["graph"].values():
            for r, i in pr:
                if r == "I": i_indices.add(i)
        return len(i_indices)


    def _normalize_default_setter_set_num_outputs(self, document):
        return len(document["graph"]["O"])


    def _normalize_default_setter_set_created(self, document):
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
