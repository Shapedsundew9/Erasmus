'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/database_table.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome
Created Date: Friday, April 24th 2020, 6:10:25 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from .database import connection, create_table, row_count, load, store
from logging import getLogger


class database_table():


    def __init__(self, logger, table, config, schema):
        self.__logger = logger
        self.__table = table
        self.__conn = connection(logger, config['dbname'], config['recreate'], config['username'], config['password'], config['host'], config['port'])
        self.__db_args = (self.__logger, self.__conn, self.__table)
        self.__columns = create_table(*self.__db_args, {k: v['meta']['database'] for k, v in schema.items()})
        self.__logger.info("%s table has %d entries.", self.__table, len(self))
            

    def __len__(self):
        return row_count(*self.__db_args)


    def load(self, query, fields=None):
        if fields is None: fields = self.__columns
        return load(*self.__db_args, query, fields, self.__columns)


    def store(self, entry):
        return store(*self.__db_args, entry)
            
            