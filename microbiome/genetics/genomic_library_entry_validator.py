'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/validation.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Sunday, March 29th 2020, 2:20:33 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from datetime import datetime
from hashlib import sha256
from json import load, loads
from logging import getLogger
from os.path import dirname, join
from pprint import pformat

from cerberus import Validator

from .gc_graph import gc_graph, ep_idx, conn_idx
from .gc_type import validate, asint, INVALID_NAME, INVALID_VALUE

NULL_GC = "0" * 64
DEAD_GC_PREFIX = "deadbeef000000000000000000000000"
with open(join(dirname(__file__), "../formats/genomic_library_entry_format.json"), "r") as file_ptr:
    _GENOMIC_LIBRARY_ENTRY_SCHEMA = schema = load(file_ptr)


def define_signature(gc):
    # The signature for a codon GC is slightly different
    string = str(gc_graph(gc['graph']))

    # If it is a codon glue on the mandatory definition
    if "generation" in gc and gc["generation"] == 0:
        if "meta_data" in gc and "function" in gc["meta_data"]:
            string += gc["meta_data"]["function"]["python3"]["0"]["inline"]
            if 'code' in gc["meta_data"]["function"]["python3"]["0"]:
                string += gc["meta_data"]["function"]["python3"]["0"]["code"]

    # Remove spaces etc. to give some degrees of freedom in formatting and
    # not breaking the signature
    return sha256("".join(string.split()).encode()).hexdigest()


class _genomic_library_entry_validator(Validator):

    # TODO: Make errors ValidationError types for full disclosure
    # https://docs.python-cerberus.org/en/stable/customize.html#validator-error

    _logger = getLogger(__name__)

    def _check_with_valid_graph(self, field, value):
        gcg = gc_graph(value)
        gcg.validate()
        for e in gcg.status: self._error(field, str(e))


    # Checks for a valid codon or non-codon

    def _check_with_valid_alpha_class(self, field, value):

        if not value:
            # Valid codon
            if "beta_class" in self.document and self.document['beta_class']:
                self._error(
                    field, "If alpha_class == 0, beta_class must == 0.")
            # if "generation" in self.document and self.document['generation']: self._error(field, "If alpha_class == 0, generation must == 0.")
            if "codon_depth" in self.document and self.document['codon_depth'] != 1:
                self._error(
                    field, "If alpha_class == 0, codon_depth must == 1.")
            if "code_depth" in self.document and self.document['code_depth'] != 1:
                self._error(
                    field, "If alpha_class == 0, code_depth must == 1.")
            if "gca" in self.document and self.document['gca'] != NULL_GC:
                self._error(
                    field, "If alpha_class == 0, gca must == " + NULL_GC)
            if "gcb" in self.document and self.document['gcb'] != NULL_GC:
                self._error(
                    field, "If alpha_class == 0, gcb must == " + NULL_GC)
            if "num_codes" in self.document and self.document['num_codes'] != 1:
                self._error(field, "If alpha_class == 0, num_codes must == 1.")
            if "num_unique_codes" in self.document and self.document['num_unique_codes'] != 1:
                self._error(
                    field, "If alpha_class == 0, num_unique_codes must == 1.")
            if "raw_num_codons" in self.document and self.document['raw_num_codons'] != 1:
                self._error(
                    field, "If alpha_class == 0, raw_num_codons must == 1.")
            if "opt_num_codons" in self.document and self.document['opt_num_codons'] != 1:
                self._error(
                    field, "If alpha_class == 0, opt_num_codons must == 1.")
            if "meta_data" in self.document and "parents" in self.document['meta_data']:
                self._error(
                    field, "If alpha_class == 0 then there are no parents.")
            if "meta_data" in self.document and not "function" in self.document['meta_data']:
                self._error(
                    field, "If alpha_class == 0 then there must be a 'function' definition.")
            elif not "python3" in self.document['meta_data']['function']:
                self._error(
                    field, "If alpha_class == 0 then there must be a 'python3' definition.")
        else:
            # Valid non-codon
            if "beta_class" in self.document and not self.document['beta_class']:
                self._error(
                    field, "If alpha_class != 0, beta_class must != 0.")
            if "meta_data" in self.document and not "parents" in self.document['meta_data']:
                self._error(
                    field, "If alpha_class != 0 then there must be at least one parent.")


    def _check_with_valid_created(self, field, value):
        try:
            date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            self._error(
                field, "Created date-time is not valid. Unknown error parsing.")
            return

        if date_time_obj > datetime.utcnow():
            self._error(field, "Created date-time cannot be in the future.")


    def _check_with_valid_gc_type(self, field, value):
        if not validate(value) and value != INVALID_VALUE:
            self._error(field, 'Does not exist')


    def _check_with_valid_inline(self, field, value):
        # TODO: Check right number of return parameters and arguments
        pass


    def _check_with_valid_callable(self, field, value):
        # TODO: Check right number of return parameters and arguments. Check arguments all have default=None.
        pass


    def _normalize_default_setter_set_signature(self, document):
        return define_signature(self.document)


    def _normalize_default_setter_set_input_types(self, document):
        # Sort the input endpoints by index then return the types as a list
        graph = gc_graph(document["graph"])
        ep_list = sorted(list(filter(graph.row_filter('I'), graph.graph.values())), key=lambda x:x[ep_idx.INDEX])
        return [ep[ep_idx.TYPE] for ep in ep_list]


    def _normalize_default_setter_set_output_types(self, document):
        return [ep[conn_idx.TYPE] for ep in document["graph"]["O"]]


    def _normalize_default_setter_set_num_inputs(self, document):
        graph = gc_graph(document["graph"])
        ep_list = list(filter(graph.row_filter('I'), graph.graph.values()))
        return len(ep_list)


    def _normalize_default_setter_set_num_outputs(self, document):
        return len(document["graph"]["O"])


    def _normalize_default_setter_set_opt_num_codons(self, document):
        return 1 if document['gca'] == NULL_GC and document['gcb'] == NULL_GC else 0


    def _normalize_default_setter_set_created(self, document):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


genomic_library_entry_validator = _genomic_library_entry_validator(_GENOMIC_LIBRARY_ENTRY_SCHEMA, purge_unknown=True)