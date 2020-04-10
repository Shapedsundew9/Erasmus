'''
Filename: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client/database.py
Path: /home/shapedsundew9/Projects/Erasmus/erasmus-gp-client
Created Date: Saturday, February 29th 2020, 4:00:40 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from psycopg2 import connect
from .genetics.entry_validator import ENTRY_VALIDATION_SCHEMA


def connection(logger, table, db, rc, user, pwd, host, port):
    conn = connect(host=host, port=port, user=user, password=pwd)
    if not conn is None:
        logger.info("Connected to postgresql.")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database;")
        list_database = cur.fetchall()
        if not db in list_database or (db in list_database and rc):
            msg = "%s database does not exist." if not rc else "Dropping %s database."
            logger.info(msg, db)
            cur.execute("DROP DATABASE IF EXISTS " + db)
            cur.execute("CREATE DATABASE " + db)
            logger.info("Created %s database.", db)
        conn.close()
        conn = connect(database=db, host=host, port=port, user=user, password=pwd)
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)", (table,))
        if not cur.fetchone()[0]:
            columns = "("
            for k ,v in ENTRY_VALIDATION_SCHEMA.items():
                c = v['meta']['database']
                null = " " if c['null'] else " NOT NULL "
                columns += k + " " + c['type'] + null + c['properties'] + ", "
            cur.execute("CREATE TABLE {0} {1}".format(table, columns[:-2] + ")"))
            logger.info("Created %s table with %s columns.", table, columns)
    else:
        logger.error("Could not connect to database %s, user = %s, password = %s, host = %s, port = %d", db, user, pwd, host, port)
    return conn
