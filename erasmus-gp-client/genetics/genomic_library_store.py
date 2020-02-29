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


CONFIG_SECTION = "local_genomic_library"
TABLE_NAME = "genomic_library"
TABLE_COLUMNS = '''(
    graph TEXT NOT NULL,
    signature TEXT PRIMARY KEY,
    generation BIGINT NOT NULL,
    references BIGINT NOT NULL,
    multi_ancestor BOOL NOT NULL,
    max_depth INTEGER NOT NULL,
    num_codes INTEGER NOT NULL,
    raw_num_codons INTEGER NOT NULL,
    opt_num_codons INTEGER,
    num_inputs INTEGER NOT NULL,
    num_outputs INTEGER NOT NULL,
    ancestor TEXT,
    classification TEXT,
    creator TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    meta_data TEXT,
)'''


class genomic_library_store():

    _db = None
    _entry_count = None
    is_empty = None
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library_store._db is None:
            db, rc, user, pwd, host, port = get_config(CONFIG_SECTION, ('dbname', 'recreate', 'user', 'password', 'host', 'port'))
            genomic_library_store._db = connection(genomic_library_store._logger, TABLE_NAME, TABLE_COLUMNS, db, rc, user, pwd, host, port)
            genomic_library_store._entry_count = self.__len__()
            genomic_library_store._logger.info("%s table has %d entries.", TABLE_NAME, genomic_library_store._entry_count)
            genomic_library_store.is_empty = genomic_library_store._entry_count == 0


    def __len__(self):
        return genomic_library_store._db.cursor().execute("SELECT COUNT(*) FROM {0}".format(TABLE_NAME)).fetchone()[0]


    def add(self, entry):
        entry.created = time()
        entry.index = genomic_library_store._entry_count
        dbcur = genomic_library_store._db.cursor()
        does_not_exist = dbcur.execute("SELECT * FROM {0} WHERE id LIKE ?".format(TABLE_NAME), (entry.id,)).fetchone() is None
        if does_not_exist:
            genomic_library_store._entry_count += 1
            dbcur.execute("INSERT INTO {0} VALUES (?,?,?,?,?,?,?)".format(TABLE_NAME),
                (entry.data, entry.id, entry.ancestor, entry.name, entry.meta_data, entry.created, entry.index))
            genomic_library_store._db.commit()
        return does_not_exist, entry.index


    def get(self, eid):
        dbcur = genomic_library_store._db.cursor()
        dbcur.execute("SELECT * FROM {0} WHERE id LIKE ?".format(TABLE_NAME), (eid,))
        return dbcur.fetchone()


    def get_by_idx(self, idx):
        dbcur = genomic_library_store._db.cursor()
        dbcur.execute("SELECT * FROM {0} WHERE idx IS ?".format(TABLE_NAME), (int(idx),))
        return dbcur.fetchone()




