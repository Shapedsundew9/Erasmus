"""Simplified database table access."""


from datetime import datetime
from zlib import compress, decompress
from pickle import dumps, loads
from copy import deepcopy
from os.path import join, dirname
from psycopg2 import connect, sql, DatabaseError, OperationalError
from .entry_column_meta_validator import entry_column_meta_validator
from .config import get_config


class database_table():
    """Connects to (or creates as needed) a postgres database & table.

    The intention of database_table is to provide a simple interface to instanciate, 
    append, update & query a persistant data store.

    Whilst database_table acts like it has complete control over the defined databases
    it does not assume that it does. Once tables are created database_table users
    need only have SELECT, INSERT & UPDATE priviliages.

    The database connection details & table definition come from the global
    configuration. Instanciation specifes only a logger and table name as a
    key into the 'tables' section of the global configuration.
    
    Only one connection per database is maintained following the design principle
    of a worker being a single threaded process.

    Database connections are created at instanciation (if not already created) and
    persisted as a key (database name): value (connection object) pair in the
    _conn dictionary.
    """

    # TODO: Need to add retry logic and emergency dump of SQL.
    #   Wrap cur.execute() in retry logic with configurable back off.
    #   Force a close() of the current connection, delete it & re-establish.
    # TODO: Need to verify privilages.
    #   1. database access as needed
    #   2. postgres database read access
    # TODO: A logger should not be mandatory.
    _conn = {}


    def __init__(self, logger, table, suppress_recreate=False):
        """Connect or create all required objects. Verify access privilages.

        Args
        ----
        logger (logger): Standard logger.
        table (str): Table name. Must be defined in the global configuration.
        suppress_recreate (bool): Will ignore the 'recreate' configuration flag if True.
        """

        self._logger = logger
        self.table = table
        config = get_config()
        # TODO: Need to me more defensive here. 'table' may not exist.
        self.dbname = config['tables'][table]['database']
        self.schema = {k: v['meta'] for k, v in config['tables'][table]['schema'].items()}
        c = config['databases'][self.dbname]
        if self.dbname not in database_table._conn:
            database_table._conn[self.dbname] = self._connection(self.dbname, c['username'], c['password'], c['host'], c['port'])
        if not database_table._conn[self.dbname] is None:
            if c['recreate'] and not suppress_recreate: self._delete_table()
            self._columns = self._create_table(config['tables'][table]['history_decimation'])
            self._logger.info("%s table has %d entries.", self.table, len(self))
            

    def __len__(self):
        """Return the number of entries in the table."""
        dbcur = database_table._conn[self.dbname].cursor()
        dbcur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(self.table)))
        retval = dbcur.fetchone()[0]
        dbcur.close()
        return retval  


    # TODO: The parameters here should be associated with the connection in _conn.
    def _connection(self, db, user, pwd, host, port):
        """Create a connection to the database."""
        try:
            conn = connect(host=host, port=port, user=user, password=pwd, dbname='postgres')
        except OperationalError as e:
            conn = None
            self._logger.fatal("Unable to connect to database %s", e)
        if not conn is None:
            self._logger.info("Connected to postgresql.")
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("SELECT datname FROM pg_database")
            list_database = cur.fetchall()
            if not (db,) in list_database:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db)))
                self._logger.info("Created %s database.", db)
            conn.close()

            # Connect to the new database & prep it as a microbiome DB
            conn = connect(host=host, port=port, user=user, password=pwd, dbname=db)
            cur = conn.cursor()
            with open(join(dirname(__file__), "microbiome.sql"), "r") as file:
                cur.execute(file.read())
            conn.commit()
            self._logger.info("Database %s prep'd for microbiome.", db)
        else:
            self._logger.error("Could not connect to database %s, user = %s, password = %s, host = %s, port = %d", db, user, pwd, host, port)
        return conn


    def _delete_db(self):
        database_table._conn[self.dbname].close()
        del database_table._conn[self.dbname]
        c = get_config()['databases'][self.dbname]
        conn = connect(dbname='postgres', user=c['username'], password=c['password'], host=c['host'], port=c['port'])
        dbcur = conn.cursor()
        conn.autocommit = True
        dbcur.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(self.dbname)))
        dbcur.close()
        conn.close()        
        self._logger.debug("Database %s dropped.", self.dbname)


    # Get the table definition 
    def _table_definition(self):
        dbcur = database_table._conn[self.dbname].cursor()
        dbcur.execute("SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s", (self.table,))
        columns = [c[0] for c in dbcur.fetchall()]
        dbcur.close()
        database_table._conn[self.dbname].commit()
        self._logger.debug("Table %s columns: %s", self.table, columns)
        return columns


    # Create the table if it does not exist else clear it.
    def _create_table(self, history_decimation={'enabled': False}):
        cur = database_table._conn[self.dbname].cursor()
        cur.execute(sql.SQL("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)"), (self.table,))
        if not cur.fetchone()[0]:

            # Create the column definitions
            columns = []
            has_cumsum = False
            for k ,c in self.schema.items():
                sql_str = " " + c['database']['type']
                if c['database']['null']: sql_str += " NOT NULL"
                if not c['database']['properties'] is None: sql_str += " " + c['database']['properties']
                columns.append(sql.Identifier(k) + sql.SQL(sql_str))
                if c['database']['cumsum']:
                    sql_str = sql.Identifier(k + '_cumsum') + sql.SQL(" " + c['database']['type'])
                    sql_str += sql.SQL(" DEFAULT 0 NOT NULL")
                    columns.append(sql_str)
                    has_cumsum = True

            # Create the table
            sql_str = sql.SQL("CREATE TABLE {} ({})").format(sql.Identifier(self.table), sql.SQL(", ").join(columns))
            self._logger.info(sql_str.as_string(database_table._conn[self.dbname]))
            cur.execute(sql_str)
            if has_cumsum:
                sql_str = sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(self.table + "_last_insert"))
                cur.execute(sql_str)
                sql_str = sql.SQL("CREATE TABLE {} ({})").format(sql.Identifier(self.table + "_last_insert"), sql.SQL(", ").join(columns))
                self._logger.info(sql_str.as_string(database_table._conn[self.dbname]))
                cur.execute(sql_str)

            # If decimation history is enabled create the triggers
            if history_decimation['enabled']:
                sql_str = sql.SQL("SELECT history_decimation_setup({}, {}, {})").format(sql.Literal(self.table),
                    sql.Literal(history_decimation['phase_size']), sql.Literal(history_decimation['num_phases']))
                self._logger.info(sql_str.as_string(database_table._conn[self.dbname]))
                cur.execute(sql_str)

            # If any of the columns are cumsum then create the triggers
            for k ,c in self.schema.items():
                if c['database']['cumsum']:
                    sql_str = sql.SQL("SELECT cumsum_setup({}, {})").format(sql.Literal(self.table), sql.Literal(k))
                    self._logger.info(sql_str.as_string(database_table._conn[self.dbname]))
                    cur.execute(sql_str)
    
            cur.close()
            database_table._conn[self.dbname].commit()
        # else:
        #   TODO: Should verify the schema matches the table definition.
        #   TODO: Verify we can SELECT, INSERT, UPDATE & DELETE as needed. 
        return self._table_definition()


    def _delete_table(self):
        cur = database_table._conn[self.dbname].cursor()
        sql_str = sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(self.table))
        cur.execute(sql_str)
        cur.close()    
        database_table._conn[self.dbname].commit()
        self._logger.info(sql_str.as_string(database_table._conn[self.dbname]))


    def _term_to_sql(self, term):
        sql_list = [sql.Identifier(term[0])]
        if isinstance(term[1], list):
            sql_list.append(sql.SQL(" IN ("))
            sql_list.append(sql.SQL(', ').join(map(sql.Literal, [self._cast_term_to_store_type(term[0], value) for value in term[1]])))
            sql_list.append(sql.SQL(")"))
        elif isinstance(term[1], dict):
            if len(term[1]) == 2 and 'min' in term[1] and 'max' in term[1]:
                # Assume this is a range for a numeric type                    
                sql_list.append(sql.SQL(" BETWEEN "))
                sql_list.append(sql.Literal(self._cast_term_to_store_type(term[0], term[1]['min'])))
                sql_list.append(sql.SQL(" AND "))
                sql_list.append(sql.Literal(self._cast_term_to_store_type(term[0], term[1]['max'])))
            else:
                # Assume this field has a codec
                # term[0] & mask = term[1]
                sql_list.append(sql.SQL(" & "))
                sql_list.append(sql.Literal(self._cast_term_to_store_type(term[0], {k: True for k in term[1].keys()})))
                sql_list.append(sql.SQL(" = "))
                sql_list.append(sql.Literal(self._cast_term_to_store_type(term[0], term[1])))
        else:
            sql_list.append(sql.SQL(" = {}").format(sql.Literal(self._cast_term_to_store_type(*term))))
        return sql.Composed(sql_list)
        

    def _query_to_sql(self, query):
        sql_terms = [self._term_to_sql(term) for term in query.items() if not term[0] in ("limit", "random", "order by")] 
        if len(sql_terms) > 1: sql_obj = sql.SQL("WHERE ") + sql.SQL(" AND ").join(sql_terms)
        elif len(sql_terms) == 1: sql_obj = sql.SQL("WHERE ") + sql_terms[0]
        else: sql_obj = sql.SQL("")
        if 'limit' in query: sql_obj += sql.SQL(" LIMIT {}").format(sql.Literal(query['limit']))
        if 'order by' in query: sql_obj += sql.SQL(" ORDER BY {}").format(sql.Identifier(query['order by']))
        return sql_obj


    def _cast_entry_to_load_type(self, data, fields):
        entry = dict(zip(fields, data))
        self._logger.debug("Storage format entry: %s", entry)
        for k, v in entry.items():
            if k in self.schema and not v is None:
                if self.schema[k]['compressed']: entry[k] = loads(decompress(v))
                elif isinstance(v, memoryview): entry[k] = v.hex()
                elif isinstance(v, datetime): entry[k] = v.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                elif 'codec' in self.schema[k]: entry[k] = {b: bool((1 << f) & entry[k]) for b, f in self.schema[k]['codec'].items() }
        self._logger.debug("Application format entry: %s", entry)
        return entry


    def isconnected(self):
        return not database_table._conn[self.dbname] is None


    def load(self, queries, fields=None, lock=False):
        if fields is None: fields = self._columns
        retval = []
        self._logger.debug("Queries are %s", str(queries))
        for query in queries:
            dbcur = database_table._conn[self.dbname].cursor(name="bill", withhold=True and not lock)
            dbcur.itersize = 1000
            self._logger.debug("Query is %s", str(query))
            query_sql = self._query_to_sql(query)
            sql_list = [sql.SQL("SELECT ")]
            sql_list.append(sql.SQL(', ').join(map(sql.Identifier, fields)))
            sql_list.append(sql.SQL(" FROM {} ").format(sql.Identifier(self.table)))
            sql_list.append(query_sql)
            if lock: sql_list.append(sql.SQL(" FOR UPDATE"))
            sql_str = sql.Composed(sql_list)
            self._logger.debug("Query SQL: %s", sql_str.as_string(database_table._conn[self.dbname]))
            dbcur.execute(sql_str)
            for row in dbcur: retval.append(self._cast_entry_to_load_type(row, fields))
            dbcur.close()
        if not lock: database_table._conn[self.dbname].commit()
        self._logger.debug("Query result: \n %s", str(retval))
        return retval


    def _cast_term_to_store_type(self, term, value):
        if self.schema[term]['compressed']: value = compress(dumps(value), 9)
        elif self.schema[term]['database']['type'] == "BYTEA": value = bytearray.fromhex(value)
        elif 'codec' in self.schema[term]:
            if isinstance(value, dict):
                bitfield = 0x0000000000000000
                for k, v in value.items():
                    if v: bitfield |= 1 << self.schema[term]['codec'][k]
                value = bitfield
        return value


    def _cast_entry_to_store_type(self, e):
        entry = deepcopy(e)
        for k, v in filter(lambda x: x[0] in self.schema, entry.items()): entry[k] = self._cast_term_to_store_type(k, v)
        return entry


    # TODO: This can be slow for a lot of values. Consider a multi-row insert.
    def store(self, entries):
        cur = database_table._conn[self.dbname].cursor()
        for e in entries:
            entry = self._cast_entry_to_store_type(e) 
            fields = sql.SQL(", ").join([sql.Identifier(k) for k in entry.keys()])
            values = sql.SQL(", ").join([sql.Literal(v) for v in entry.values()])
            sql_str = sql.SQL("INSERT INTO {} ({}) VALUES ({}) ON CONFLICT DO NOTHING").format(sql.Identifier(self.table), fields, values)
            self._logger.debug(sql_str.as_string(database_table._conn[self.dbname]))
            try:
                cur.execute(sql_str)
            except (Exception, DatabaseError) as ex:
                self._logger.error("Failed to store entry in DB: %s: %s", ex, sql_str.as_string(database_table._conn[self.dbname]))
                self._logger.info("All entries rolled back")
                database_table._conn[self.dbname].rollback()
                return False
        try:
            cur.close()
            database_table._conn[self.dbname].commit()
        except (Exception, DatabaseError) as ex:
            self._logger.error("Failed to store entries in DB: %s", ex)
            database_table._conn[self.dbname].rollback()
            return False
        return True


    # TODO: This can be slow for a lot of values. Consider a multi-row insert.
    def update(self, entries, keys):
        cur = database_table._conn[self.dbname].cursor()
        for e, condition in zip(entries, keys):
            entry = self._cast_entry_to_store_type(e) 
            fields = sql.SQL(", ").join([sql.SQL(" = ").join((sql.Identifier(k), sql.Literal(v))) for k, v in entry.items()])
            pairs = [sql.SQL(" = ").join((sql.Identifier(k), sql.Literal(v))) for k,v in condition.items()]
            conditions = pairs[0] if len(pairs) == 1 else sql.SQL(" AND ").join(pairs)
            sql_str = sql.SQL("UPDATE {} SET {} WHERE {}").format(sql.Identifier(self.table), fields, conditions)
            self._logger.debug(sql_str.as_string(database_table._conn[self.dbname]))
            try:
                cur.execute(sql_str)
            except (Exception, DatabaseError) as ex:
                self._logger.error("Failed to update entry in DB: %s: %s", ex, sql_str.as_string(database_table._conn[self.dbname]))
                self._logger.info("All entries rolled back")
                database_table._conn[self.dbname].rollback()
                return False
        try:
            cur.close()
            database_table._conn[self.dbname].commit()
        except (Exception, DatabaseError) as ex:
            self._logger.error("Failed to store entries in DB: %s", ex)
            database_table._conn[self.dbname].rollback()
            return False
        return True
