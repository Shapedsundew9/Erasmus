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
from hashlib import sha256
from logging import getLogger


NULL_GC = "0" * 64
DEAD_GC_PREFIX = "deadbeef000000000000000000000000"


#TODO: Add and entry format JSON validator for the meta data
class genomic_library_entry_validator(Validator):


    # TODO: Make errors ValidationError types for full disclosure
    # https://docs.python-cerberus.org/en/stable/customize.html#validator-error

    __logger = getLogger(__name__)


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

        # There must be at least one output from A
        found_a_output = False
        keys = ('B', 'O') if 'B' in value else ('O')
        for pr in keys:
            for r, i in value[pr]: found_a_output = found_a_output or r == "A" 
        if not found_a_output: self._error(field, "Missing at least one reference to A output")

        # If B exists there must be at least one output
        if "B" in value:
            found_b_output = False
            for r, i in value['O']: found_b_output = found_b_output or r == "B" 
            if not found_b_output: self._error(field, "Missing at least one reference to B output")

        # If C does exist index references must be in range
        if "C" in value:
            c_len = len(value["C"])
            for pr in value.keys():
                if pr != "C":
                    for r, i in value[pr]:
                        if r == "C" and i >= c_len:
                            self._error(field, "Reference into C from {} out of bounds. Max index = {}: [{},{}]".format(pr, c_len, r, i))

        # All values in "C" must be referenced at least once
        if "C" in value:
            actual_indices = set()
            for pr in value.keys():
                if pr != "C":
                    for r, i in value[pr]:
                        if r == "C": actual_indices.add(i)
            expected_indices = set(range(len(value["C"])))
            for i in actual_indices - expected_indices: self._error(field, "Index {} is out of range for 'C'".format(i))
            for i in expected_indices - actual_indices: self._error(field, "Index {} was expected in 'C'".format(i))

        # References to I must start at 0 and be contiguous
        actual_indices = set()
        for pr in value.keys():
            if pr != "C":
                for r, i in value[pr]:
                    if r == "I": actual_indices.add(i)
        expected_indices = set(range(max(actual_indices))) if len(actual_indices) > 0 else set()
        for i in expected_indices - actual_indices: self._error(field, "Index {} was expected in 'I'".format(i))

        # 'D's mark deleted references that were not fixed.
        for pr in value.keys():
            if pr != "C":
                for idx, (r, _) in enumerate(value[pr]):
                    if r == "D": self._error(field, "Field: '{}' Index: {} was deleted.".format(pr, idx))
            

    # Checks for a valid codon or non-codon
    def _check_with_valid_alpha_class(self, field, value):

        if not value:
            # Valid codon
            if "beta_class" in self.document and self.document['beta_class']: self._error(field, "If alpha_class == 0, beta_class must == 0.")
            # if "generation" in self.document and self.document['generation']: self._error(field, "If alpha_class == 0, generation must == 0.")
            if "codon_depth" in self.document and self.document['codon_depth'] != 1: self._error(field, "If alpha_class == 0, codon_depth must == 1.")
            if "code_depth" in self.document and self.document['code_depth'] != 1: self._error(field, "If alpha_class == 0, code_depth must == 1.")
            if "gca" in self.document and self.document['gca'] != NULL_GC: self._error(field, "If alpha_class == 0, gca must == " + NULL_GC)
            if "gcb" in self.document and self.document['gcb'] != NULL_GC: self._error(field, "If alpha_class == 0, gcb must == " + NULL_GC)
            if "num_codes" in self.document and self.document['num_codes'] != 1: self._error(field, "If alpha_class == 0, num_codes must == 1.")
            if "num_unique_codes" in self.document and self.document['num_unique_codes'] != 1: self._error(field, "If alpha_class == 0, num_unique_codes must == 1.")
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
            if "meta_data" in self.document and not "parents" in self.document['meta_data']: self._error(field, "If alpha_class != 0 then there must be at least one parent.")


    def _check_with_valid_created(self, field, value):
        try:
            date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            self._error(field, "Created date-time is not valid. Unknown error parsing.")
            return

        if date_time_obj > datetime.utcnow():
            self._error(field, "Created date-time cannot be in the future.")


    def _check_with_valid_inline(self, field, value):
        # TODO: Check right number of return parameters and arguments
        pass


    def _check_with_valid_callable(self, field, value):
        # TODO: Check right number of return parameters and arguments. Check arguments all have default=None.
        pass


    def _normalize_default_setter_set_signature(self, document):

        # The signature for a codon GC is slightly different
        string = str(self.document["graph"]["A"]) + str(self.document["graph"]["O"])
        string += self.document["gca"] + self.document["gcb"]
        if "B" in self.document["graph"]: string += str(self.document["graph"]["B"])
        if "C" in self.document["graph"]: string += str(self.document["graph"]["C"])

        # If it is a codon glue on the mandatory definition
        if "generation" in self.document and self.document["generation"] == 0:
            if "meta_data" in self.document and "function" in self.document["meta_data"]:
                string += self.document["meta_data"]["function"]["python3"]["0"]["inline"]

        # Remove spaces etc. to give some degrees of freedom in formatting and
        # not breaking the signature
        return sha256("".join(string.split()).encode()).hexdigest()


    def _normalize_default_setter_set_num_inputs(self, document):
        i_indices = set()
        for pr in document["graph"].keys():
            if pr != 'C':
                for r, i in document["graph"][pr]:
                    if r == "I": i_indices.add(i)
        return len(i_indices)


    def _normalize_default_setter_set_num_outputs(self, document):
        return len(document["graph"]["O"])


    def _normalize_default_setter_set_created(self, document):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
