'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library_store.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:39:13 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from psycopg2 import connect, DatabaseError
from time import time
from slugify import slugify
from os.path import exists
from os import remove
from .config import get_config
from logging import getLogger


CONFIG_SECTION = "local_genomic_library"
TABLE_NAME = "genetic_codes"
TABLE_COLUMNS = '''(
    data TEXT NOT NULL,
    id TEXT NOT NULL PRIMARY KEY,
    ancestor TEXT,
    name TEXT,
    meta_data TEXT,
    created REAL NOT NULL,
    idx INTEGER NOT NULL UNIQUE
)'''


class genomic_library_store():

    _db = None
    _entry_count = None
    is_empty = None
    _logger = getLogger(__name__)


    def __init__(self):
        if genomic_library_store._db is None:
            db, rc, user, pwd, host, port = get_config(CONFIG_SECTION, ('dbname', 'recreate', 'user', 'password', 'host', 'port'))
            conn = connect(host=host, port=port, user=user, password=pwd)
            genomic_library_store._logger.info("Connected to postgresql.")
            if not conn is None:
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute("SELECT datname FROM pg_database;")
                list_database = cur.fetchall()
                if not db in list_database or (db in list_database and rc):
                    msg = "%s database does not exist." if not rc else "Dropping %s database."
                    genomic_library_store._logger.info(msg, db)
                    cur.execute("DROP DATABASE IF EXISTS " + db)
                    cur.execute("CREATE DATABASE " + db)
                    genomic_library_store._logger.info("Created %s database.", db)
                cur.execute("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)", (TABLE_NAME,))
                if not cur.fetchone()[0]:
                    cur.execute("CREATE TABLE {0} {1}".format(TABLE_NAME, TABLE_COLUMNS))
                    genomic_library_store._logger.info("Created %s table.", TABLE_NAME)
            genomic_library_store._db = conn
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




