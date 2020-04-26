'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/database_table.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome
Created Date: Friday, April 24th 2020, 6:10:25 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from psycopg2 import connect, sql, DatabaseError
from datetime import datetime
from zlib import compress, decompress
from pickle import dumps, loads
from copy import deepcopy
from .entry_column_meta_validator import entry_column_meta_validator


class database_table():


    def __init__(self, logger, table, config, entry_validation_schema):
        self.__logger = logger
        self.table = table
        self.schema = {k: entry_column_meta_validator.normalized(v['meta']) for k, v in entry_validation_schema.items()}
        self.__conn = self.__connection(config['dbname'], config['username'], config['password'], config['host'], config['port'])
        if config['recreate']: self.__delete_table()
        self.__columns = self.__create_table()
        self.__logger.info("%s table has %d entries.", self.table, len(self))
            

    def __len__(self):
        # TODO: There must be a faster way
        dbcur = self.__conn.cursor()
        dbcur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(self.table)))
        retval = dbcur.fetchone()[0]
        dbcur.close()
        return retval  


    # Create the database if it does not exist and return a connection to it.
    # If rc is True the table is deleted a recreated.
    def __connection(self, db, user, pwd, host, port):
        conn = connect(host=host, port=port, user=user, password=pwd, dbname='postgres')
        if not conn is None:
            self.__logger.info("Connected to postgresql.")
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("SELECT datname FROM pg_database")
            list_database = cur.fetchall()
            if not (db,) in list_database:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db)))
                self.__logger.info("Created %s database.", db)
        else:
            self.__logger.error("Could not connect to database %s, user = %s, password = %s, host = %s, port = %d", db, user, pwd, host, port)
        return conn


    # Get the table definition 
    def __table_definition(self):
        dbcur = self.__conn.cursor()
        dbcur.execute("SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s", (self.table,))
        columns = [c[0] for c in dbcur.fetchall()]
        dbcur.close()
        self.__conn.commit()
        self.__logger.debug("Table %s columns: %s", self.table, columns)
        return columns


    # Create the table if it does not exist else clear it.
    def __create_table(self):
        cur = self.__conn.cursor()
        cur.execute(sql.SQL("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)"), (self.table,))
        if not cur.fetchone()[0]:
            columns = []
            for k ,c in self.schema.items():
                sql_str = " " + c['database']['type']
                if c['database']['null']: sql_str += " NOT NULL"
                if not c['database']['properties'] is None: sql_str += " " + c['database']['properties']
                columns.append(sql.Identifier(k) + sql.SQL(sql_str))
            sql_str = sql.SQL("CREATE TABLE {} ({})").format(sql.Identifier(self.table), sql.SQL(", ").join(columns))
            self.__logger.info(sql_str.as_string(self.__conn))
            cur.execute(sql_str)
            cur.close()
            self.__conn.commit()
        return self.__table_definition()


    def __delete_table(self):
        cur = self.__conn.cursor()
        sql_str = sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(self.table))
        cur.execute(sql_str)
        cur.close()    
        self.__conn.commit()
        self.__logger.info(sql_str.as_string(self.__conn))


    def __term_to_sql(self, term):
        sql_list = [sql.Identifier(term[0])]
        if isinstance(term[1], list):
            sql_list.append(sql.SQL(" IN ("))
            sql_list.append(sql.SQL(', ').join(map(sql.Literal, [self.__cast_term_to_store_type(term[0], value) for value in term[1]])))
            sql_list.append(sql.SQL(")"))
        elif isinstance(term[1], dict):
            sql_list.append(sql.SQL(" BETWEEN "))
            sql_list.append(sql.Literal(self.__cast_term_to_store_type(term[0], term[1]['min'])))
            sql_list.append(sql.SQL(" AND "))
            sql_list.append(sql.Literal(self.__cast_term_to_store_type(term[0], term[1]['max'])))
        else:
            sql_list.append(sql.SQL(" = {}").format(sql.Literal(self.__cast_term_to_store_type(*term))))
        return sql.Composed(sql_list)
        

    def __query_to_sql(self, query):
        sql_terms = [self.__term_to_sql(term) for term in query.items() if not term[0] in ("limit", "random")] 
        sql_obj = sql.SQL(" AND ").join(sql_terms)
        if 'limit' in query: sql_obj += sql.SQL(" LIMIT {}").format(sql.Literal(query['limit']))
        return sql_obj


    def __cast_entry_to_load_type(self, data):
        entry = dict(zip(self.__columns, data))
        for k, v in entry.items():
            if self.schema[k]['compressed']: entry[k] = loads(decompress(v))
            elif isinstance(v, memoryview): entry[k] = v.hex()
            elif isinstance(v, datetime): entry[k] = v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return entry


    def load(self, queries, fields=None):
        if fields is None: fields = self.__columns
        retval = []
        for query in queries:
            dbcur = self.__conn.cursor(name="bill", withhold=True)
            dbcur.itersize = 1000
            query_sql = self.__query_to_sql(query)
            self.__logger.debug("Query SQL: %s", query_sql.as_string(self.__conn))
            sql_list = [sql.SQL("SELECT ")]
            sql_list.append(sql.SQL(', ').join(map(sql.Identifier, fields)))
            sql_list.append(sql.SQL(" FROM {} WHERE ").format(sql.Identifier(self.table)))
            sql_list.append(query_sql)
            dbcur.execute(sql.Composed(sql_list))
            for row in dbcur: retval.append(self.__cast_entry_to_load_type(row))
            dbcur.close()
        self.__conn.commit()
        return retval


    def __cast_term_to_store_type(self, term, value):
        if self.schema[term]['compressed']: value = compress(dumps(value), 9)
        elif self.schema[term]['database']['type'] == "BYTEA": value = bytearray.fromhex(value)
        return value


    def __cast_entry_to_store_type(self, e):
        entry = deepcopy(e)
        for k, v in entry.items(): entry[k] = self.__cast_term_to_store_type(k, v)
        return entry


    def store(self, entries):
        cur = self.__conn.cursor()
        for e in entries:
            entry = self.__cast_entry_to_store_type(e) 
            fields = sql.SQL(", ").join([sql.Identifier(k) for k in entry.keys()])
            values = sql.SQL(", ").join([sql.Literal(v) for v in entry.values()])
            sql_str = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(sql.Identifier(self.table), fields, values)
            self.__logger.debug(sql_str.as_string(self.__conn))
            try:
                cur.execute(sql_str)
            except (Exception, DatabaseError) as ex:
                self.__logger.error("Failed to store entry in DB: %s: %s", ex, sql_str.as_string(self.__conn))
                self.__logger.info("All entries rolled back")
                self.__conn.rollback()
                return False
        try:
            cur.close()
            self.__conn.commit()
        except (Exception, DatabaseError) as ex:
            self.__logger.error("Failed to store entries in DB: %s", ex)
            self.__conn.rollback()
            return False
        return True