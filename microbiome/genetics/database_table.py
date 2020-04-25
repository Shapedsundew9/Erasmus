'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/database_table.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome
Created Date: Friday, April 24th 2020, 6:10:25 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from psycopg2 import connect, sql, DatabaseError
from datetime import datetime


class database_table():


    def __init__(self, logger, table, config, entry_validation_schema):
        self.__logger = logger
        self.table = table
        self.schema = {k: v['meta']['database'] for k, v in entry_validation_schema.items()}
        self.__conn = self.__connection(config['dbname'], config['username'], config['password'], config['host'], config['port'])
        if config['recreate']: self.__delete_table()
        self.__columns = self.__create_table()
        self.__logger.info("%s table has %d entries.", self.table, len(self))
            

    def __len__(self):
        # TODO: There must be a faster way
        dbcur = self.__conn.cursor()
        dbcur.execute("SELECT COUNT(*) FROM {0}".format(sql.Identifier(self.table)))
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
            if not db in list_database:
                cur.execute("CREATE DATABASE %s", db)
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
        self.__logger.debug("Table %s columns: %s", self.table, columns)
        return columns


    # Create the table if it does not exist else clear it.
    def __create_table(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)", (self.table,))
        if not cur.fetchone()[0]:
            columns = []
            for k ,c in self.schema.items():
                null = "" if c['null'] else " NOT NULL"
                properties = ", " if c['properties'] is None else " " + c['properties'] + ", "
                columns.extend([sql.Identifier(k) + sql.SQL(" " + c['type'] + null + properties)])
            cur.execute("CREATE TABLE {} ({})".format(sql.Identifier(self.table), sql.SQL(", ").join(columns)))
            cur.close()
            self.__conn.commit()
            self.__logger.info("Created %s table with %s columns.", self.table, columns)
        return self.__table_definition()


    def __delete_table(self):
        cur = self.__conn.cursor()
        cur.execute("DELETE FROM %s", (self.table,))
        cur.close()    
        self.__conn.commit()


    def __term_to_sql(self, term):
        sql_list = [sql.Identifier(term[0])]
        if isinstance(term[1], list):
            sql_list.append(sql.SQL(" IN ("))
            sql_list.append(sql.SQL(', ').join(map(sql.Literal, term[1])))
            sql_list.append(")")
        elif isinstance(term[1], dict):
            sql_list.append(sql.SQL(" BETWEEN "))
            sql_list.append(sql.SQL("to_timestamp({})").format(sql.Literal(term[1]['min'])) if isinstance(term[1]['min'], str) else sql.Literal(term[1]['min']))
            sql_list.append(sql.SQL(" AND "))
            sql_list.append(sql.SQL("to_timestamp({})").format(sql.Literal(term[1]['max'])) if isinstance(term[1]['max'], str) else sql.Literal(term[1]['max']))
        else:
            sql_list.append(sql.Literal(term[1]))
        return sql.Composed(sql_list)
        

    def __query_to_sql(self, query):
        sql_terms = [self.__term_to_sql(term) for term in query.items()] 
        sql_obj = sql.SQL(" AND ").join(sql_terms)
        if 'limit' in query: sql_obj += sql.SQL(" LIMIT {}").format(sql.Literal(query['limit']))
        return sql_obj


    def load(self, query, fields):
        dbcur = self.__conn.cursor()
        query_sql = self.__query_to_sql(query)
        self.__logger.debug("Query SQL: %s", query_sql.as_string(self.__conn))
        sql_list = [sql.SQL("SELECT ")]
        sql_list.append(sql.SQL(', ').join(map(sql.Identifier, fields)))
        sql_list.append(sql.SQL(" FROM {} WHERE ").format(sql.Identifier(self.table)))
        sql_list.append(query_sql)
        dbcur.execute(sql.Composed(sql_list))
        data = dbcur.fetchall()
        dbcur.close()
        if not data is None:
            retval = []
            while data:
                datum = data.pop()
                row = {}
                for k, v in zip(self.__columns, datum):
                    if isinstance(v, memoryview): v = bytes(v)
                    elif isinstance(v, datetime): v = v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    row[k] = v
                retval.append(row)
            return retval
        return None    


    def store(self, entry):
        fields = sql.SQL(", ").join([sql.Identifier(k) for k in entry.keys()])
        values = sql.SQL(", ").join([sql.Literal(v) for v in entry.values()])
        sql_str = sql.SQL("INSERT INTO {} ({}) VALUES ({})".format(sql.Identifier(self.table), fields, values))
        try:
            cur = self.__conn.cursor()
            cur.execute(sql_str)
            cur.close()
            self.__conn.commit()
        except (Exception, DatabaseError) as ex:
            self.__logger.error("Failed to store DB entry: %s", ex)
            return False
        return True