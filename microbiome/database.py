'''
Filename: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client/database.py
Path: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client
Created Date: Saturday, February 29th 2020, 4:00:40 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from psycopg2 import connect, sql
from datetime import datetime


# Create the database if it does not exist and return a connection to it.
# If rc is True the database is deleted a recreated.
def connection(logger, db, rc, user, pwd, host, port):
    conn = connect(host=host, port=port, user=user, password=pwd, dbname='postgres')
    if not conn is None:
        logger.info("Connected to postgresql.")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database")
        list_database = cur.fetchall()
        if not db in list_database or (db in list_database and rc):
            msg = "%s database does not exist." if not rc else "Dropping %s database."
            logger.info(msg, db)
            cur.execute("DROP DATABASE IF EXISTS " + db)
            cur.execute("CREATE DATABASE " + db)
            logger.info("Created %s database.", db)
    else:
        logger.error("Could not connect to database %s, user = %s, password = %s, host = %s, port = %d", db, user, pwd, host, port)
    return conn


# Get the table definition 
def __table_definition(logger, conn, table):
    dbcur = conn.cursor()
    dbcur.execute("SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{0}'".format(_LIBRARY_TABLE))
    columns = [c[0] for c in dbcur.fetchall()]
    dbcur.close()
    format_str = ""
    for c in columns: format_str += "%s, "
    format_str = format_str[:-2]
    columns_str = ""
    for c in columns: columns_str += c + ", "
    columns_str = columns_str[:-2]
    logger.debug("Table %s columns: %s", table, columns)
    logger.debug("Table %s columns_str: %s", table, columns_str)
    logger.debug("Table %s format_str: %s", table, format_str)
    return columns, columns_str, format_str


# Create the table if it does not exist else clear it.
def create_table(logger, conn, table, schema):
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)", (table,))
    if not cur.fetchone()[0]:
        columns = "("
        for k ,c in schema.items():
            null = "" if c['null'] else " NOT NULL"
            properties = ", " if c['properties'] is None else " " + c['properties'] + ", "
            columns += k + " " + c['type'] + null + properties
        cur.execute("CREATE TABLE {0} {1}".format(table, columns[:-2] + ")"))
        cur.close()
        conn.commit()
        logger.info("Created %s table with %s columns.", table, columns)
    else:
        cur.execute("DELETE FROM %s", (table,))
        cur.close()
    return __table_definition(logger, conn, table)


def row_count(logger, conn, table):
    # TODO: There must be a faster way
    dbcur = conn.cursor()
    dbcur.execute("SELECT COUNT(*) FROM {0}".format(table))
    retval = dbcur.fetchone()[0]
    dbcur.close()
    return retval  


def __term_to_sql(term):
    sql_list = [sql.Identifier(term[0])]
    if isinstance(term[1], list):
        sql_list.append(sql.SQL(" IN ("))
        sql_list.append(sql.SQL(', ').join(map(sql.Literal, term[1])))
        sql.append(")")
    elif isinstance(term[1], dict):
        sql_list.append(sql.SQL(" BETWEEN "))
        sql_list.append(sql.SQL("to_timestamp({})").format(sql.Literal(term[1]['min'])) if isinstance(term[1]['min'], str) else sql.Literal(term[1]['min']))
        sql_list.append(sql.SQL(" AND "))
        sql_list.append(sql.SQL("to_timestamp({})").format(sql.Literal(term[1]['max'])) if isinstance(term[1]['max'], str) else sql.Literal(term[1]['max']))
    else:
        sql_list.append(sql.Literal(term[1]))
    return sql.Composed(sql_list)
    

def __query_to_sql(query):
    sql_list = []
    sql_terms = [__term_to_sql(term) for term in query.items()] 
    sql_obj = sql.SQL(" AND ").join(sql_terms)
    if 'limit' in query: sql_obj += sql.SQL(" LIMIT {}").format(sql.Literal(query['limit'])))
    return sql_obj


def load(logger, conn, table, query, fields, columns):
    dbcur = conn.cursor()
    query_sql = __query_to_sql(query)
    logger.debug("Query SQL: %s", query_sql.as_string(conn))
    sql_list = [sql.SQL("SELECT ")]
    sql_list.append(sql.SQL(', ').join(map(sql.Identifier, fields)))
    sql_list.append(sql.SQL(" FROM {} WHERE ").format(sql.Identifier(table)))
    sql_list.append(query_sql)
    dbcur.execute(sql.Composed(sql_list))
    data = dbcur.fetchall()
    dbcur.close()
    if not data is None:
        retval = []
        while data:
            datum = data.pop()
            row = {}
            for k, v in zip(columns, datum):
                if isinstance(v, memoryview): v = bytes(v)
                elif isinstance(v, datetime): v = v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                row[k] = v
            retval.append(row)
    return None    


