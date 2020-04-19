'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library_store.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:39:13 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from datetime import datetime
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
    _columns = None
    _columns_str = ""
    _format = ""


    def __init__(self):
        if genomic_library_store._db_library is None:
            db, rc, user, pwd, host, port = get_config(_CONFIG_SECTION, ('dbname', 'recreate', 'username', 'password', 'host', 'port'))
            genomic_library_store._db_library = connection(genomic_library_store._logger, _LIBRARY_TABLE, db, rc, user, pwd, host, port)
            dbcur = genomic_library_store._db_library.cursor()
            dbcur.execute("SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{0}'".format(_LIBRARY_TABLE))
            genomic_library_store._columns = [c[0] for c in dbcur.fetchall()]
            dbcur.close()
            for c in genomic_library_store._columns: genomic_library_store._format += "%s, "
            genomic_library_store._format = genomic_library_store._format[:-2]
            for c in genomic_library_store._columns: genomic_library_store._columns_str += c + ", "
            genomic_library_store._columns_str = genomic_library_store._columns_str[:-2]
            genomic_library_store._logger.info("%s table has %d entries.", _LIBRARY_TABLE, len(self))


    def __len__(self):
        # TODO: There must be a faster way
        dbcur = genomic_library_store._db_library.cursor()
        dbcur.execute("SELECT COUNT(*) FROM {0}".format(_LIBRARY_TABLE))
        retval = dbcur.fetchone()[0]
        dbcur.close()
        return retval



    # signature is a hex string with no prefix
    # TODO: Also support a byte array
    def __getitem__(self, signature):
        dbcur = genomic_library_store._db_library.cursor()
        dbcur.execute("SELECT {0} FROM {1} WHERE signature = %s".format(genomic_library_store._columns_str, _LIBRARY_TABLE), ("\\x" + signature,))
        data = dbcur.fetchone()
        dbcur.close()
        if not data is None:
            retval = {}
            for k, v in zip(genomic_library_store._columns, data):
                if isinstance(v, memoryview):
                    v = bytes(v)
                elif isinstance(v, datetime):
                    v = v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                retval[k] = v
            return retval
        return None


    def load(self, query, fields="*"):
        dbcur = genomic_library_store._db_library.cursor()
        try:
            dbcur.execute("SELECT * FROM {0} WHERE {1}".format(_LIBRARY_TABLE, query_str), query_param)
        except (Exception, DatabaseError) as ex:
            genomic_library_store._logger.error("Failed to get entries for query %s, %s: %s", query_str, query_param, ex)
            return None
        retval = dbcur.fetchall()
        dbcur.close()
        return retval


    def store(self, entry, settime=False):
        if settime: entry['created'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        does_not_exist = self[entry['signature'].hex()] is None
        if does_not_exist:
            vals = [entry[k] for k in genomic_library_store._columns]
            try:
                cur = genomic_library_store._db_library.cursor()
                cur.execute("INSERT INTO {0}({1}) VALUES ({2})".format(_LIBRARY_TABLE, genomic_library_store._columns_str, genomic_library_store._format), vals)
                cur.close()
                genomic_library_store._db_library.commit()
            except (Exception, DatabaseError) as ex:
                genomic_library_store._logger.error("Failed to store entry %s: %s", entry['signature'], ex)
                return False
            return True
        return False
            
            
