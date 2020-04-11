'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library_store.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:39:13 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from time import time
from ..database import connection
from .config import get_config
from logging import getLogger
from psycopg2 import DatabaseError


_CONFIG_SECTION = "local_genomic_library"
_LIBRARY_TABLE = "genomic_library"
_DB_TYPE_MAP = {
    "integer": {"fmt": "%d", "zero": 0},
    "bigint":  {"fmt": "%d", "zero": 0},
    "bytea":  {"fmt": "'\\x%s'", "zero": "0"},
    "character varying": {"fmt": "%s", "zero": "0"},
    "timestamp without time zone": {"fmt": "to_timestamp(%f)", "zero": 0.0},
    "real": {"fmt": "%f", "zero": 0.0}
}

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


    _db_library = None
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library_store._db_library is None:
            db, rc, user, pwd, host, port = get_config(_CONFIG_SECTION, ('dbname', 'recreate', 'username', 'password', 'host', 'port'))
            genomic_library_store._db_library = connection(genomic_library_store._logger, _LIBRARY_TABLE, db, rc, user, pwd, host, port)
            genomic_library_store._logger.info("%s table has %d entries.", _LIBRARY_TABLE, len(self))


    def __len__(self):
        # TODO: There must be a faster way
        dbcur = genomic_library_store._db_library.cursor()
        dbcur.execute("SELECT COUNT(*) FROM {0}".format(_LIBRARY_TABLE))
        return dbcur.fetchone()[0]


    # signature is a hex string with no prefix
    # TODO: Also support a byte array
    def __getitem__(self, signature):
        dbcur = genomic_library_store._db_library.cursor()
        dbcur.execute("SELECT * FROM {0} WHERE signature = %s".format(_LIBRARY_TABLE), ("\\x" + signature,))
        return dbcur.fetchone()


    def get_signatures(self, query_str, query_param=[]):
        dbcur = genomic_library_store._db_library.cursor()
        try:
            dbcur.execute("SELECT signature FROM {0} WHERE {1}".format(_LIBRARY_TABLE, query_str), query_param)
        except (Exception, DatabaseError) as ex:
            genomic_library_store._logger.error("Failed to get signatures for query %s, %s: %s", query_str, query_param, ex)
            return None
        return dbcur.fetchall()


    def get_entries(self, query_str, query_param=[]):
        dbcur = genomic_library_store._db_library.cursor()
        try:
            dbcur.execute("SELECT * FROM {0} WHERE {1}".format(_LIBRARY_TABLE, query_str), query_param)
        except (Exception, DatabaseError) as ex:
            genomic_library_store._logger.error("Failed to get entries for query %s, %s: %s", query_str, query_param, ex)
            return None
        return dbcur.fetchall()


    def store(self, entry, settime=True):
        if settime: entry['created'] = time()
        does_not_exist = self[entry['signature']] is None
        if does_not_exist:
            cols, fmts, vals = "", "", []
            for k, v in entry.items():
                cols += k + ", "
                fmts += "%s, "
                vals.append(v)
            try:
                print("INSERT INTO {0}({1}) VALUES ({2})".format(_LIBRARY_TABLE, cols[:-2], fmts[:-2]))
                print(vals)
                genomic_library_store._db_library.cursor().execute("INSERT INTO {0}({1}) VALUES ({2})".format(_LIBRARY_TABLE, cols[:-2], fmts[:-2]), vals)
            except (Exception, DatabaseError) as ex:
                genomic_library_store._logger.error("Failed to store entry %s: %s", entry['signature'], ex)
                return False
            return True
        return False
            
            
