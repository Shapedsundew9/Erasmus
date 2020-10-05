'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:33:43 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from ..database_table import database_table
from logging import getLogger
from .genomic_library_entry_validator import genomic_library_entry_validator
from .codon_validator import codon_validator
from ..query_validator import query_validator
from pprint import pformat
from ..config import get_config
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


    _store = None
    _codon_validator = None
    _entry_validator = None
    _query_validator = None
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library._store is None:
            table_name = get_config()['genomic_library']['table']
            genomic_library._store = database_table(genomic_library._logger, table_name)
            genomic_library._codon_validator = codon_validator(load(open(join(dirname(__file__), "../formats/codon_format.json"), "r")))
            genomic_library._entry_validator = genomic_library_entry_validator(get_config()['tables'][table_name]['schema'], purge_unknown=True)
            genomic_library._query_validator = query_validator(genomic_library._entry_validator.schema)
            genomic_library._query_validator.table_name = table_name
            if not len(genomic_library._store): self._initialise()


    def _initialise(self):
        # TODO: Look for the biome first
        self._entry_zero()
        genomic_library._logger.info("Loading codon library")
        if not self._load_codons("codon_library.json"):
            genomic_library._logger.error("Codon library failed validation. Unable to initialise genomic library.")
            exit(1)
        genomic_library._logger.info("Loading mutation primitive codon library")
        if not self._load_codons("gc_mutation_library.json"):
            genomic_library._logger.error("GC mutation library failed validation. Unable to initialise genomic library.")
            exit(1)
        genomic_library._logger.info("Loading query primitive codon library")
        if not self._load_codons("gc_query_library.json"):
            genomic_library._logger.error("GC query library failed validation. Unable to initialise genomic library.")
            exit(1)
        

    def _load_codons(self, src_file_name):
        codons = []
        for raw_codon in load(open(join(dirname(__file__), "codon_library.json"), "r")):
            if not genomic_library._codon_validator.validate(raw_codon):
                genomic_library._logger.error("Codon invalid.\n%s\n%s", pformat(raw_codon), pformat(genomic_library._codon_validator.errors))
                return False
            codons.append(genomic_library._codon_validator.normalized(raw_codon))
        return self.store(codons)


    def _len_(self):
        return len(genomic_library._store)


    # A zero entry is needed for genetic codes that do not have a GCA or GCB
    def _entry_zero(self):
        entry = {}
        for k, v in genomic_library._entry_validator.schema.items():
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
        genomic_library._store.store([entry])


    # Return an application formatted entry from the store
    def __getitem__(self, signature):
        value = genomic_library._store.load([{"signature": signature}])
        return None if value is None else value[0]


    # Return a list of application formatted entries from the store that meet the query
    def load(self, query, fields=None):
        if not genomic_library._query_validator.validate(query):
            genomic_library._logger.warning("Query is not valid:\n%s\n%s", pformat(genomic_library._query_validator.errors), pformat(query))
            return []
        query = genomic_library._query_validator.normalized(query)
        return genomic_library._store.load(query, fields)


    def normalize(self, entries):
        if isinstance(entries, list):
            for i, entry in enumerate(entries):
                if self.validate(entry)[0]:
                    entries[i] = genomic_library._entry_validator.normalized(entry)
                    if not self._calculate_fields(entries[i], entries): return False
                else:
                    genomic_library._logger.debug("Entry %s is not valid. No entries will be stored.", entries[i])
                    return False
        else:
            if self.validate(entries)[0]:
                entries.update(genomic_library._entry_validator.normalized(entries))
                if not self._calculate_fields(entries, [entries]): return False
            else:
                genomic_library._logger.debug("Entry %s is not valid. No entries will be stored.", entries)
                return False
        return True


    # Store a new application formatted entry.
    def store(self, entries):
        return genomic_library._store.store(entries) if self.normalize(entries) else False


    # Validates an application format entry and populates fields that do not
    # require store lookups to calculate.
    def validate(self, entry):
        if not genomic_library._entry_validator(entry):
            err_txt = genomic_library._entry_validator.errors
            genomic_library._logger.debug("Entry is not valid:\n%s\n%s", pformat(err_txt), pformat({k: v for k, v in entry.items() if k[:2] != '_'}))
            return False, err_txt 
        return True, []


    # Some fields depend on GCA & GCB which must be defined in either the genomic library or the entries to be added.
    def _calculate_fields(self, entry, entries=None):
        # TODO: Need to update gca & gcb if necessary.
        gca = self[entry['gca']] if entries is None or not entry['gca'] in entries else entries[entry['gca']]
        if gca is None: genomic_library._logger.warning("gca %s does not exist.",entry['gca'])
        gcb = self[entry['gcb']] if entries is None or not entry['gcb'] in entries else entries[entry['gcb']]
        if gcb is None: genomic_library._logger.warning("gcb %s does not exist.",entry['gcb'])
        if gca is None or gcb is None: return False
        entry['code_depth'] = max((gca['code_depth'], gcb['code_depth'])) + 1
        entry['num_codes'] = max((gca['num_codes'] + gcb['num_codes'], 1))
        entry['raw_num_codons'] = max((gca['raw_num_codons'] + gcb['raw_num_codons'], 1))
        entry['generation'] = max(max((gca['generation'], gcb['generation'])) + 1, entry['generation'])
        for k, v in gca['properties'].items():
            if k in entry['properties']: entry['properties'][k] = entry['properties'][k] or v
        for k, v in gcb['properties'].items():
            if k in entry['properties']: entry['properties'][k] = entry['properties'][k] or v
        return True
