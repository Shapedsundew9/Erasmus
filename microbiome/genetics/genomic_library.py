'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:33:43 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from .database_table import database_table
from logging import getLogger
from .genomic_library_entry_validator import genomic_library_entry_validator
from .query_validator import query_validator
from pprint import pprint, pformat
from .config import get_config
from os.path import dirname, join
from json import load


# The genomic_library is responsible for:
#   1. Persisting entries
#   2. Converting entries from application format to storage format
#   3. Converting entries from storage format to application format
#   4. Populating calculable entry fields
#   4. Validating entries to be added to the store
#   5. Retrieving entries based on criteria
class genomic_library():


    __store = None
    __entry_validator = genomic_library_entry_validator
    __query_validator = query_validator(genomic_library_entry_validator.schema)
    __logger = getLogger(__name__)


    def __init__(self, __table_name="genomic_library"):
        if genomic_library.__store is None:
            genomic_library.__store = database_table(genomic_library.__logger, __table_name,
                get_config(["data_stores", __table_name]), genomic_library.__entry_validator.schema)
            genomic_library.__query_validator.table_name = __table_name
        if not len(genomic_library.__store): self.__initialise()


    def __initialise(self):
        # TODO: Look for the biome first
        self.__entry_zero()
        if not self.store(load(open(join(dirname(__file__), "codon_library.json"), "r"))):
            genomic_library.__logger.error("Codon library failed validation. Unable to initialised genomic library.")
            exit(1)


    def __len__(self):
        return len(genomic_library.__store)


    # A zero entry is needed for genetic codes that do not have a GCA or GCB
    def __entry_zero(self):
        entry = {}
        for k, v in genomic_library.__entry_validator.schema.items():
            if v['meta']['database']['type'] == "BYTEA":
                value = '0' * v['minlength'] if "minlength" in v else '00'
            elif v['meta']['database']['type'] == "INTEGER" or v['meta']['database']['type'] == "BIGINT":
                value = 0
            elif v['meta']['database']['type'] == "TIMESTAMP":
                value = "2000-01-01T00:00:00.000001Z" 
            elif v['meta']['database']['type'] == "REAL":
                value = 0.0
            else:
                value = "entry_zero"
            if 'codec' in v['meta']: value = {}
            entry[k] = value
        genomic_library.__store.store([entry])


    # Return an application formatted entry from the store
    def __getitem__(self, signature):
        value = genomic_library.__store.load([{"signature": signature}])
        return None if value is None else value[0]


    # Return a list of application formatted entries from the store that meet the query
    def load(self, query, fields=None):
        if not genomic_library.__query_validator.validate(query):
            genomic_library.__logger.warning("Query is not valid:\n%s\n%s", pformat(genomic_library.__query_validator.errors), pformat(query))
            return []
        query = genomic_library.__query_validator.normalized(query)
        return genomic_library.__store.load(query, fields)


    # Store a new application formatted entry.
    # TODO: Implement a bulk store.
    def store(self, entries):
        if not isinstance(entries, list): entries = list(entries)
        for i in range(len(entries)): 
            if self.validate(entries[i]):
                entries[i] = genomic_library.__entry_validator.normalized(entries[i])
                if not self.__calculate_fields(entries[i]): return False
            else:
                genomic_library.__logger.debug("Entry %s is not valid. No entries will be stored.", entries[i]['signature'])
                return False
        return genomic_library.__store.store(entries)


    # Validates an application format entry and populates fields that do not
    # require store lookups to calculate.
    def validate(self, entry):
        if not genomic_library.__entry_validator(entry):
            err_txt = genomic_library.__entry_validator.errors
            genomic_library.__logger.debug("Entry is not valid:\n%s\n%s", pformat(err_txt), pformat(entry))
            return False
        return True


    def __calculate_fields(self, entry):
        # TODO: Need to update gca & gcb if necessary.
        gca = self[entry['gca']]
        if gca is None: genomic_library.__logger.warning("gca %s does not exist.",entry['gca'])
        gcb = self[entry['gcb']]
        if gcb is None: genomic_library.__logger.warning("gcb %s does not exist.",entry['gcb'])
        if gca is None or gcb is None: return False
        entry['code_depth'] = max((gca['code_depth'], gcb['code_depth'])) + 1
        entry['num_codes'] = gca['num_codes'] + gcb['num_codes']
        entry['raw_num_codons'] = gca['raw_num_codons'] + gcb['raw_num_codons']
        entry['generation'] = max((gca['generation'], gcb['generation'])) + 1
        entry['properties'] = gca['properties']
        for k, v in gcb['properties'].items():
            if k in entry['properties']: entry['properties'][k] = entry['properties'][k] or v
        return True
