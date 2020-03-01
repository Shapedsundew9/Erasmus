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


CONFIG_SECTION = "local_genomic_library"
LIBRARY_TABLE = "genomic_library"
LIBRARY_COLUMNS = '''(
    graph BYTEA NOT NULL,
    signature BYTEA PRIMARY KEY,
    generation BIGINT NOT NULL,
    references BIGINT NOT NULL,
    code_depth INTEGER NOT NULL,
    num_codes INTEGER NOT NULL,
    num_unique_codes INTEGER NOT NULL,
    raw_num_codons INTEGER NOT NULL,
    opt_num_codons INTEGER,
    num_inputs INTEGER NOT NULL,
    num_outputs INTEGER NOT NULL,
    classification BIGINT NOT NULL,
    creator BYTEA NOT NULL,
    created TIMESTAMP NOT NULL,
    meta_data BYTEA NOT NULL
)'''

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
            db, rc, user, pwd, host, port = get_config(CONFIG_SECTION, ('dbname', 'recreate', 'user', 'password', 'host', 'port'))
            genomic_library_store._db_library = connection(genomic_library_store._logger, LIBRARY_TABLE, LIBRARY_COLUMNS, db, rc, user, pwd, host, port)
            genomic_library_store._logger.info("%s table has %d entries.", LIBRARY_TABLE, len(self))


    def __len__(self):
        return genomic_library_store._db_library.cursor().execute("SELECT COUNT(*) FROM {0}".format(LIBRARY_TABLE)).fetchone()[0]


    def __getitem__(self, signature):
        dbcur = genomic_library_store._db_library.cursor()
        dbcur.execute("SELECT * FROM {0} WHERE signature = %s".format(LIBRARY_TABLE), (signature,))
        return dbcur.fetchone()


    def get_signatures(self, query_str, query_param):
        dbcur = genomic_library_store._db_library.cursor()
        try:
            dbcur.execute("SELECT signature FROM {0} WHERE {1}".format(LIBRARY_TABLE, query_str), query_param)
        except (Exception, DatabaseError) as ex:
            genomic_library_store._logger.error("Failed to get signatures for query %s, %s: %s", query_str, query_param, ex)
            return None
        return dbcur.fetchall()


    def get_entries(self, query_str, query_param):
        dbcur = genomic_library_store._db_library.cursor()
        try:
            dbcur.execute("SELECT * FROM {0} WHERE {1}".format(LIBRARY_TABLE, query_str), query_param)
        except (Exception, DatabaseError) as ex:
            genomic_library_store._logger.error("Failed to get entries for query %s, %s: %s", query_str, query_param, ex)
            return None
        return dbcur.fetchall()


    def __setitem__(self, signature, entry):
        entry.created = time()
        does_not_exist = self[entry.signature] is None
        if does_not_exist:
            genomic_library_store._db_library.cursor().execute(
                "INSERT INTO {0} VALUES (%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,to_timestamp(%f),%s)".format(LIBRARY_TABLE),
                (entry.graph, entry.signature, entry.generation, entry.references, entry.code_depth, entry.num_codes, entry.num_unique_codes,
                 entry.raw_num_codons, entry.opt_num_codons, entry.num_inputs, entry.num_outputs, entry.classification, entry.creator, entry.created,
                 entry.meta_data))
        else:
            genomic_library_store._db_library.cursor().execute("""UPDATE {0} SET generation = %d, references = %d,
                opt_num_codons = %d, classification = %d, meta_data = %s WHERE signature = %s""".format(LIBRARY_TABLE), (entry.generation,
                entry.references, entry.opt_num_codons, entry.classification, entry.meta_data, entry.signature))
            genomic_library_store._db_library.commit()
