-- Needed for NEW column parameterisation.
CREATE EXTENSION IF NOT EXISTS hstore;

CREATE OR REPLACE FUNCTION history_decimation_ait()
    RETURNS TRIGGER
    SET SCHEMA 'public'
	SET client_min_messages = error
    LANGUAGE plpgsql
    AS $$
	DECLARE
		__phase RECORD;
		__hdti_table TEXT := 'history_decimation_table_index';
		__idx_name TEXT;
		__table RECORD;
		__idx BIGINT;
    BEGIN
		-- How This Works
		-- ==============
		-- A history decimation table automatically reduces the stored sample frequency of older
		-- samples as a way of managing size. There are some restrictions on what can be a history
		-- decimation table: Specifically, the rows inserted must be indexed by an integer sequence
		-- that increments by 1 and, to make any sense, the data in each row should be independent
		-- of any other row.
		-- A history decimation table stores 1 << phase_size rows per historical "phase". phase_size and
		-- the number of phases are therefore small positive integers that are not going to cause 
		-- numerical overflow. When it is full the table will store (1 << phase_size) * num_phases rows.
		-- Each "phase" of the table history is a sequence of rows with different degrees of decimation.
		-- The "decimation" is not decimation in the strict sense of the word but in the common usage of
		-- it. The decimation of each phase is defined by keeping every (1 << phase)th sample. i.e.
		--      Phase 0: 1 << 0 = 1 i.e. keep all samples
		--		Phase 1: 1 << 1 = 2 i.e. keep every other sample
		--		Phase 2: 1 << 2 = 4 i.e. keep every 4th sample
		--		...
		--		Phase N: 1 << N = 2^(N-1) i.e. keep every 2^(N-1)th sample.
		-- Each phase (will eventually) contain the same number of rows which provides the expanding
		-- history period. Phases do not overlap and so the maximum history range stored is:
		--		(1 << (phase_size + num_phases)) - (1 << phase_size)  
		-- Conceptually the phases work like a series of stacks where new rows are pushed into the first
		-- stack filling it up until the ((1 << phase_size) + 1)th row is inserted
		-- which pushes the oldest row out of the bottom. If that row is a (1 << phase)th row then it is
		-- pushed into the next stack, if it is not then it is deleted. Every row pushed out the bottom
		-- of the last stack (phase) is deleted.
		EXECUTE format ('SELECT * FROM history_decimation_table_index WHERE table_name = %L LIMIT 1', TG_ARGV[0]) INTO __table;
		__idx := (hstore(NEW) -> __table.idx_name)::BIGINT;
		
		-- Step through phase table.
		-- For each phase check if the index pushed out of the previous stack should be
		-- put into the next. If not we are done.
		FOR __phase IN 0..(__table.num_phases - 1) LOOP 
			IF __idx & ((1::BIGINT << __phase) - 1) = 0 THEN
				__idx := __idx - (1::BIGINT << (__table.phase_size + __phase));
				IF __idx < 0 THEN RETURN NULL; END IF;					
			ELSE
				EXECUTE 'DELETE FROM ' || TG_ARGV[0] || ' WHERE ' || __table.idx_name || ' = ' || __idx;
				RETURN NULL;
			END IF;
		END LOOP;

		-- DELETE all rows dropping out the bottom of the last phase
		EXECUTE 'DELETE FROM ' || TG_ARGV[0] || ' WHERE ' || __table.idx_name || ' = ' || __idx;
		RETURN NULL;
    END;
    $$;

-- See https://dba.stackexchange.com/questions/90555/postgresql-select-primary-key-as-serial-or-bigserial/90567#90567
-- Kudos https://dba.stackexchange.com/users/3684/erwin-brandstetter
CREATE OR REPLACE FUNCTION elaborate_data_types(__table_name TEXT)
    RETURNS TABLE (id TEXT, name TEXT, type TEXT)
    SET SCHEMA 'public'
	SET client_min_messages = error
    LANGUAGE plpgsql
    AS $body$
	BEGIN
	RETURN QUERY EXECUTE format('
		SELECT a.attrelid::regclass::text, a.attname::text
			 , CASE WHEN a.atttypid = ANY (''{int,int8,int2}''::regtype[])
				  AND EXISTS (
					 SELECT FROM pg_attrdef ad
					 WHERE  ad.adrelid = a.attrelid
					 AND    ad.adnum   = a.attnum
					 AND    pg_get_expr(ad.adbin, ad.adrelid)
						  = ''nextval(''''''
						 || (pg_get_serial_sequence (a.attrelid::regclass::text
												  , a.attname))::regclass
						 || ''''''::regclass)''
					 )
				THEN CASE a.atttypid
						WHEN ''int''::regtype  THEN ''serial''
						WHEN ''int8''::regtype THEN ''bigserial''
						WHEN ''int2''::regtype THEN ''smallserial''
					 END
				ELSE format_type(a.atttypid, a.atttypmod)
				END AS data_type
		FROM   pg_attribute  a
		WHERE  a.attrelid = ''%I''::regclass  -- table name, optionally schema-qualified
		AND    a.attnum > 0
		AND    NOT a.attisdropped
		ORDER  BY a.attnum;', __table_name);
END;
$body$;


CREATE TABLE IF NOT EXISTS history_decimation_table_index
	("table_name" TEXT PRIMARY KEY, "phase_size" INTEGER, "num_phases" INTEGER, "idx_name" TEXT);


DROP FUNCTION IF EXISTS history_decimation_setup(text,integer,integer);
CREATE OR REPLACE FUNCTION history_decimation_setup(__table_name TEXT, __phase_size INTEGER, __num_phases INTEGER)
    RETURNS BOOLEAN
    SET SCHEMA 'public'
    LANGUAGE plpgsql
    AS $$
	DECLARE
	   	__phase INTEGER := 0;
		__hdti_table TEXT := 'history_decimation_table_index';
		__trigger TEXT := __table_name || '_ait';
		__trigger_function TEXT := 'history_decimation_ait';
		__idx_name TEXT;
    BEGIN

	-- No crazy numbers
	-- TODO: This could be serial size aware & return a useful exception
	IF (__num_phases < 1) OR (__num_phases > 8) OR (__phase_size < 1) OR (__phase_size > 23) THEN
		RAISE EXCEPTION 'Number or size of phases out of range.' USING HINT = '0 < num_phases < 9 & 0 < phase_size < 24';
		RETURN FALSE;
	END IF; 

	-- Table must exist
	IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = __table_name) THEN
		RAISE EXCEPTION 'Table "%" does not exist.', __table_name;
		RETURN FALSE;
	END IF;
	
	-- Must have at least one serial index. If there are multiple prefer longer sequences
	-- and if there are multiple of those choose the first in alphabetical order of name
	SELECT name INTO __idx_name FROM elaborate_data_types(__table_name) WHERE type IN ('smallserial', 'serial', 'bigserial')
		ORDER BY type ASC, name ASC LIMIT 1;
	IF __idx_name IS NULL THEN
		RAISE EXCEPTION 'No smallserial, serial or bigserial column was found in table "%"', __table_name;
		RETURN FALSE;
	END IF;

    EXECUTE format ('DELETE FROM history_decimation_table_index WHERE table_name = %L', __table_name);
	
	EXECUTE format ('INSERT INTO history_decimation_table_index ("table_name", "phase_size", "num_phases", "idx_name")
					VALUES (%L, %L, %L, %L);', __table_name, __phase_size, __num_phases, __idx_name);
	EXECUTE format ('DROP TRIGGER IF EXISTS %I on %I;', __trigger, __table_name);
	EXECUTE format ('CREATE TRIGGER %I AFTER INSERT ON %I FOR EACH ROW EXECUTE PROCEDURE %I(%L);',
					__trigger, __table_name, __trigger_function, __table_name);
	RETURN TRUE;
END;
$$;


DROP FUNCTION IF EXISTS cumsum_setup(text, text);
CREATE OR REPLACE FUNCTION cumsum_setup(__table_name TEXT, __column_name TEXT)
    RETURNS BOOLEAN
    SET SCHEMA 'public'
    LANGUAGE plpgsql
    AS $$
	DECLARE
		__cumsum_trigger TEXT := __table_name || '_' || __column_name || '_cumsum_bit';
		__cumsum_trigger_function TEXT := __table_name || '_' || __column_name || '_cumsum_bit';
		__last_insert_trigger TEXT := __table_name || '_last_insert_ait';
		__last_insert_trigger_function TEXT := __table_name || '_last_insert_ait';
		__last_record RECORD;
    BEGIN

	-- Table must exist
	IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = __table_name) THEN
		RAISE EXCEPTION 'Table "%" does not exist.', __table_name;
		RETURN FALSE;
	END IF;

	-- Create a table for the last row inserted, a trigger & trigger function to populate it
	EXECUTE format ('DROP TABLE IF EXISTS %I', __table_name || '_last_insert');
	EXECUTE format ('CREATE TABLE %I AS TABLE %I WITH NO DATA', __table_name || '_last_insert', __table_name);
	EXECUTE format ('INSERT INTO %I (%I) VALUES (0)', __table_name || '_last_insert', __column_name || '_cumsum');
	EXECUTE format ('DROP TRIGGER IF EXISTS %I on %I;', __last_insert_trigger, __table_name);
	EXECUTE format ('CREATE OR REPLACE FUNCTION %I()
    				 RETURNS TRIGGER
    				 SET SCHEMA ''public''
					 SET client_min_messages = error
    				 LANGUAGE plpgsql
    				 AS $body$
    				 BEGIN
					 	DELETE FROM %I;
						INSERT INTO %I SELECT (NEW).*;
					 	RETURN NULL;
    				 END;
    				 $body$;', __last_insert_trigger_function, __table_name || '_last_insert', __table_name || '_last_insert');
	EXECUTE format ('CREATE TRIGGER %I AFTER INSERT ON %I FOR EACH ROW EXECUTE PROCEDURE %I();',
					__last_insert_trigger, __table_name, __last_insert_trigger_function);

	-- Create a trigger & trigger function to do the cumulative summing
	EXECUTE format ('DROP TRIGGER IF EXISTS %I on %I;', __cumsum_trigger, __table_name);
	EXECUTE format ('CREATE OR REPLACE FUNCTION %I()
    				 RETURNS TRIGGER
    				 SET SCHEMA ''public''
					 SET client_min_messages = error
    				 LANGUAGE plpgsql
    				 AS $body$
					 DECLARE
					 	__last_insert RECORD;
    				 BEGIN
					 	SELECT * FROM %I LIMIT 1 INTO __last_insert;
					 	NEW.%I := __last_insert.%I + NEW.%I;
					 	RETURN NEW;
    				 END;
    				 $body$;', __cumsum_trigger_function, __table_name || '_last_insert', __column_name || '_cumsum', __column_name || '_cumsum', __column_name);
	EXECUTE format ('CREATE TRIGGER %I BEFORE INSERT ON %I FOR EACH ROW EXECUTE PROCEDURE %I();',
					__cumsum_trigger, __table_name, __cumsum_trigger_function);
	RETURN TRUE;
END;
$$;