"""The Genomic Library class wraps the database_table.""" 

from pprint import pformat
from json import load
from os.path import dirname, join
from logging import getLogger, DEBUG
from functools import lru_cache
from .genomic_library_entry_validator import genomic_library_entry_validator, NULL_GC
from ..query_validator import query_validator
from ..text_token import text_token, register_token_code
from ..config import get_config
from ..database_table import database_table


_NULL_GC_DATA = {
    'code_depth': 0,
    'num_codes': 0,
    'raw_num_codons': 1,
    'generation': 0,
    'properties': {},
    '_stored': True
}


register_token_code('E03000', 'Query is not valid: {errors}: {query}')
register_token_code('E03001', 'Entry is not valid: {errors}: {entry}')
register_token_code('E03002', 'Referenced GC(s) {references} do not exist. Entry:\n{entry}:')


class genomic_library():
    """The genomic_library is responsible for:
        1. Populating calculable entry fields
        2. Validating entries to be added to the store
        3. Validating table queries.

        Class Members
        -------------
        _store (database_table): Persistent storage for the genetic codes.
        _entry_validator (genomic_library_entry_validator):
        _query_validator (query_validator): Using the _entry_validator schema.
        _logger (logger):
    """

    _store = None
    _query_validator = None
    _logger = getLogger(__name__)
    _verify_consistency = None


    def __init__(self):
        """Multiple instances point to the same class assets."""
        if genomic_library._store is None:
            genomic_library._verify_consistency = get_config()['general']['verify_consistency']
            table_name = get_config()['genomic_library_table']
            genomic_library._logger.debug("Genomic library table name: {}".format(table_name))
            genomic_library._store = database_table(genomic_library._logger, table_name)
            schema = get_config()['tables'][table_name]['schema']
            genomic_library._query_validator = query_validator(schema)
            genomic_library._query_validator.table_name = table_name


    def __len__(self):
        """Return the number of entries in the library.
        
        Returns
        -------
        (int) The number of rows in the genomic_library_table table.
        """
        return len(genomic_library._store)


    # Return an application formatted entry from the store
    @lru_cache(maxsize=1024)
    def __getitem__(self, signature):
        """Fetch an entry using its unique signature.
        
        Args
        ----
        signature (str): SHA256 string.

        Returns
        -------
        (dict) Genetic code 
        """
        value = genomic_library._store.load([{"signature": signature}])
        return None if not value else value[0]


    def _check_references(self, references, check_list=None):
        """Verify all the references exist in the genomic library.

        Genetic codes reference each other. A debugging check is to verify the 
        existence of all the references.

        Args
        ----
        references(list): List of genetic code signatures to look up.
        check_list(set): A set of known existing genetic codes signatures.

        Returns
        -------
        Empty list if all references exist else the signatures of missing references.
        """
        if check_list is None: check_list = set([NULL_GC])
        naughty_list = []
        for reference in references:
            if self[reference] is None and not reference in check_list:
                naughty_list.append(reference)
            else:
                check_list.add(reference)
        return naughty_list


    def isconnected(self):
        """Verify the genetic library has access to the database."""
        return genomic_library._store.isconnected()
        

    def load(self, query, fields=None):
        """Fetch the genetic codes fields for those rows matching the query.

        Args
        ----
        query(dict): A query dictionary object.
        fields(list): A list of fields to return for each matching genetic code.

        Returns
        -------
        (list) A List of genetic code dictionaries.
        """
        query = genomic_library._query_validator.normalized(query)
        if genomic_library._logger.getEffectiveLevel() == DEBUG and not genomic_library._query_validator.validate(query):
            genomic_library._logger.error(str(text_token({'E03000': {
                'errors': pformat(genomic_library._query_validator.errors, width=180),
                'query': pformat(query, width=180)}})))
            return []
        return genomic_library._store.load(query, fields)


    def _calculate_fields(self, entry, entries=None):
        """Calculate the derviced genetic code fields.
        
        Cerberus normalisation can only set fields based on the contents of the genetic code dictionary.
        However, some fields are derived from GCA & GCB. Entries may be stored in batch and so
        may reference other, as yet to be stored, genetic code dictionaries.

        The entry dictionary is modified.

        Args
        ----
        entry(dict): A genetic code dictionary.
        entries(list): A list of genetic code dictionaries not yet stored in the genomic library.
        """

        # TODO: Need to update gca & gcb if necessary.
        if entries is None or not entry['gca'] in entries:
            gca = self[entry['gca']]
        else:
            gca = entries[entry['gca']]
            if not gca['_stored']: self._calculate_fields(gca, entries)

        if entries is None or not entry['gcb'] in entries:
            gcb = self[entry['gcb']]
        else:
            gcb = entries[entry['gcb']]
            if not gcb['_stored']: self._calculate_fields(gcb, entries)

        if gca is None and entry['gca'] == NULL_GC: gca = _NULL_GC_DATA
        if gcb is None and entry['gcb'] == NULL_GC: gcb = _NULL_GC_DATA

        entry['code_depth'] = max((gca['code_depth'], gcb['code_depth'])) + 1
        entry['num_codes'] = max((gca['num_codes'] + gcb['num_codes'], 1))
        entry['raw_num_codons'] = max((gca['raw_num_codons'] + gcb['raw_num_codons'], 1))
        entry['generation'] = max(max((gca['generation'], gcb['generation'])) + 1, entry['generation'])
        for k, v in gca['properties'].items():
            if k in entry['properties']: entry['properties'][k] = entry['properties'][k] or v
        for k, v in gcb['properties'].items():
            if k in entry['properties']: entry['properties'][k] = entry['properties'][k] or v


    def _normalize(self, entries):
        normalized_entries = []
        genomic_library._logger.debug("Normalizing entries.")
        for entry in entries:
            normalized_entries.append(genomic_library_entry_validator.normalized(entry))
            self._calculate_fields(normalized_entries[-1], normalized_entries)
        if genomic_library._logger.getEffectiveLevel() == DEBUG:
            genomic_library._logger.debug("Validating normalised entries before storing.")
            for entry in normalized_entries:
                if not genomic_library_entry_validator.validate(entry):
                    print(genomic_library_entry_validator.document)
                    genomic_library._logger.error(str(text_token({'E03001': {
                        'errors': pformat(genomic_library_entry_validator.errors, width=180),
                        'entry': pformat(entry, width=180)}})))
        if genomic_library._verify_consistency:
            genomic_library._logger.debug("Checking entry consistency before storing.")
            for entry in normalized_entries:
                references = [entry['gca'], entry['gcb']]
                if 'parents' in entry['meta_data']:
                    for parents in entry['meta_data']['parents']:
                        references.extend(parents)
            problem_references = self._check_references(references, set([entry['signature'] for entry in normalized_entries]))
            if problem_references:
                genomic_library._logger.error(str(text_token({'E03002': {
                    'entry': pformat(entry, width=180),
                    'references': problem_references}})))
        return normalized_entries


    # Store a new application formatted entry.
    def store(self, entries):
        return genomic_library._store.store(self._normalize(entries))


    def update(self, entries, conditions):
        return genomic_library._store.update(entries, conditions)
