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
    _format_str = "("
    _format_lst = []


    def __init__(self):
        if genomic_library_store._db_library is None:
            db, rc, user, pwd, host, port = get_config(_CONFIG_SECTION, ('dbname', 'recreate', 'user', 'password', 'host', 'port'))
            genomic_library_store._db_library = connection(genomic_library_store._logger, _LIBRARY_TABLE, db, rc, user, pwd, host, port)
            cur = genomic_library_store._db_library.cursor()
            cur.execute("SELECT column_name, data_type from information_schema.columns WHERE table_name='%s')", (_LIBRARY_TABLE,))
            genomic_library_store._columns = {c[0]: c[1] for c in cur.fetchall()}
            for k, v in genomic_library_store._columns:
                if v == 'integer' or v = 'bigint': fmtr = "%d"
                if v == 'bytea' or v == 'character varying': fmtr = "%s"
                if v == 'timestamp without time zone': fmtr = "to_timestamp(%f)"
                if v == 'real': fmtr = "%f"
                genomic_library_store._format_lst.append(k)
                genomic_library_store._format_str += fmtr + ","
            genomic_library_store._format_str = genomic_library_store._format_str[:-1] + ")"
            genomic_library_store._logger.info("%s table has %d entries.", _LIBRARY_TABLE, len(self))


    def __len__(self):
        return genomic_library_store._db_library.cursor().execute("SELECT COUNT(*) FROM {0}".format(_LIBRARY_TABLE)).fetchone()[0]


    # signature is a hex string with no prefix
    # TODO: Also support a byte array
    def __getitem__(self, signature):
        dbcur = genomic_library_store._db_library.cursor()
        dbcur.execute("SELECT * FROM {0} WHERE signature = '\x%s'".format(_LIBRARY_TABLE), (signature,))
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
            dbcur.execute("SELECT * FROM {0} WHERE {1}".format(LIBRARY_TABLE, query_str), query_param)
        except (Exception, DatabaseError) as ex:
            genomic_library_store._logger.error("Failed to get entries for query %s, %s: %s", query_str, query_param, ex)
            return None
        return dbcur.fetchall()


    def store(self, entry):
        entry.created = time()
        does_not_exist = self[entry.signature] is None
        if does_not_exist:
            entry_list = [entry[k] for k in genomic_library_store._format_lst]
            genomic_library_store._db_library.cursor().execute(
                "INSERT INTO {0} VALUES {1}".format(LIBRARY_TABLE, genomic_library_store._format_str), entry_list)
        else:
            genomic_library_store._db_library.cursor().execute("""UPDATE {0} SET generation = %d, references = %d,
                opt_num_codons = %d, classification = %d, meta_data = %s WHERE signature = %s""".format(LIBRARY_TABLE), (entry.generation,
                entry.references, entry.opt_num_codons, entry.classification, entry.meta_data, entry.signature))
            genomic_library_store._db_library.commit()
