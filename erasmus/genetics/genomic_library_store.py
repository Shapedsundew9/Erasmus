'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetics/genomic_library_store.py
Path: /home/shapedsundew9/Projects/Erasmus/src/genetics
Created Date: Friday, January 10th 2020, 10:39:13 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


import sqlite3
import time
from slugify import slugify
from os.path import exists
from os import remove


TABLE_NAME = 'genomic_library'
TABLE_COLUMNS = '(data TEXT NOT NULL, id TEXT NOT NULL PRIMARY KEY,ancestor TEXT, name TEXT, \
    meta_data TEXT, created REAL NOT NULL, idx INTEGER NOT NULL UNIQUE)'


class genomic_library_store():

    _db = None
    name = None
    _entry_count = None
    is_empty = None


    def __init__(self, name=TABLE_NAME, recreate=False, temp=False):
        if self._db is None: 
            self.name = name
            filename = slugify(name) + '.db'
            if recreate and exists(filename): remove(filename)
            mode = 'memory' if temp else 'rwc'
            db_uri = 'file:' + filename + '?mode=' + mode
            self._db = sqlite3.connect(db_uri, uri=True)
            if self._is_empty(): 
                dbcur = self._db.cursor() 
                dbcur.execute("""CREATE TABLE {0}{1}""".format(TABLE_NAME, TABLE_COLUMNS))
            self._entry_count = self.__len__()
            self.is_empty = self._entry_count == 0



    def __len__(self):
        return self._db.cursor().execute("""SELECT COUNT(*) FROM {0}""".format(TABLE_NAME)).fetchone()[0]


    def _is_empty(self):
        dbcur = self._db.cursor()
        dbcur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'""".format(TABLE_NAME))
        return dbcur.fetchone() is None


    def add(self, entry):
        entry.created = time.time()
        entry.index = self._entry_count
        dbcur = self._db.cursor()
        does_not_exist = dbcur.execute('SELECT * FROM {0} WHERE id LIKE ?'.format(TABLE_NAME), (entry.id,)).fetchone() is None
        if does_not_exist:
            self._entry_count += 1
            dbcur.execute('INSERT INTO {0} VALUES (?,?,?,?,?,?,?)'.format(TABLE_NAME),
                (entry.data, entry.id, entry.ancestor, entry.name, entry.meta_data, entry.created, entry.index))
            self._db.commit()
        return does_not_exist, entry.index


    def get(self, eid):
        dbcur = self._db.cursor()
        dbcur.execute('SELECT * FROM {0} WHERE id LIKE ?'.format(TABLE_NAME), (eid,))
        return dbcur.fetchone()


    def get_by_idx(self, idx):
        dbcur = self._db.cursor()
        print(idx)
        dbcur.execute('SELECT * FROM {0} WHERE idx IS ?'.format(TABLE_NAME), (int(idx),))
        return dbcur.fetchone()




