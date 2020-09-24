'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/entry_column_meta_validator.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Saturday, April 25th 2020, 5:33:07 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from cerberus import Validator
from datetime import datetime
from hashlib import sha256
from json import dumps


class population_validator(Validator):

    def _check_with_valid_created(self, field, value):
        try:
            date_time_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            self._error(field, "Created date-time is not valid. Unknown error parsing.")
            return

        if date_time_obj > datetime.utcnow():
            self._error(field, "Created date-time cannot be in the future.")


    # TODO:
    def _check_with_valid_population_count(self, field, value):
        pass


    # TODO:
    def _check_with_valid_population_dict(self, field, value):
        pass


    # TODO:
    def _check_with_valid_cull_parameters(self, field, value):
        pass


    # TODO:
    def _check_with_valid_evolution_parameters(self, field, value):
        pass


    # TODO:
    def _check_with_valid_genomic_library_query(self, field, value):
        pass


    # TODO: Harden this
    def _normalize_default_setter_set_signature(self, document):
        #sig_str = dumps(self.document['cull_parameters']) + dumps(self.document['evolution_parameters']) + self.document['predecessor']
        sig_str = dumps(self.document['name'])

        # Remove spaces etc. to give some degrees of freedom in formatting and
        # not breaking the signature
        return sha256("".join(sig_str.split()).encode()).hexdigest()


    def _normalize_default_setter_set_created(self, document):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
