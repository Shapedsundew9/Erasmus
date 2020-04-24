'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library_store.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:39:13 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from datetime import datetime
from ..database import connection, create_table, row_count, load, store
from .config import get_config
from logging import getLogger
from .entry_validator import ENTRY_VALIDATION_SCHEMA as SCHEMA


__CONFIG_SECTION = "local_genomic_library"
__LIBRARY_TABLE = "genomic_library"


# The genomic_library_store is responsible for
#   1. Estabilishing a connection to the database
#   2. Creating an empty library table if none exists
#   3. Writing genomic library entries and populating the 'created' time field at the time of creation
#   4. Reading genomic library entries
#   5. Providing basic aggregate statistics about the library e.g. number of entries.
# It is NOT responsible for
#   1. Formatting the entries
#   2. Validating the entries
class genomic_library_store():


    __db_library = None
    __logger = getLogger(__name__)
    __columns = None


    def __init__(self):
        if genomic_library_store.__db_library is None:
            config = get_config(__CONFIG_SECTION)
            genomic_library_store.__db_library = connection(genomic_library_store.__logger, config['dbname'], 
                config['recreate'], config['username'], config['password'], config['host'], config['port'])
            self.__db_args = (genomic_library_store.__logger, genomic_library_store.__db_library, __LIBRARY_TABLE)
            genomic_library_store.__columns = create_table(*self.__db_args, {k: v['meta']['database'] for k, v in SCHEMA.items()})
            genomic_library_store.__logger.info("%s table has %d entries.", __LIBRARY_TABLE, len(self))
            

    def __len__(self):
        return row_count(*self.__db_args)


    # signature is a hex string with no prefix
    # TODO: Also support a byte array
    def __getitem__(self, signature):
        return load(*self.__db_args, {"signature": signature}, genomic_library_store.__columns ,genomic_library_store.__columns)


    def load(self, query, fields=genomic_library_store.__columns):
        return load(*self.__db_args, query, fields, genomic_library_store.__columns)


    def store(self, entry, settime=False):
        if settime: entry['created'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        does_not_exist = self[entry['signature'].hex()] is None
        if does_not_exist: store(*self.__db_args, entry)
            
            
