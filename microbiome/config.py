"""
Manages the global configuration.

The global configuration defines the postgresql database(s) to use and how to access them.
It defines the tables in the databases, properties of the tables and which validation to use.
All values have defaults defined by the Cerberus validation schema.
"""

from json import load, dump
from logging import getLogger
from os.path import dirname, join
from pprint import pformat
from copy import deepcopy
from cerberus import Validator
from .base_validator import BaseValidator
from .entry_column_meta_validator import entry_column_meta_validator
from .platform_info_validator import platform_info_validator
from .work_registry_validator import work_registry_validator
from .worker_registry_validator import worker_registry_validator
from .work_log_validator import work_log_validator
from .text_token import text_token, register_token_code
from .genetics.genomic_library_entry_validator import genomic_library_entry_validator


_CONFIG_FORMAT_FILE = 'formats/config_format.json'
_config = {}
_logger = getLogger(__name__)
_errors = {}


register_token_code('E02000', 'Database "{database}" is not defined in the [databases] section.')
register_token_code('E02001', 'No "Meta" key found in schema field "{field}".')
register_token_code('E02002', '"Meta" key value schema field "{field}" is invalid:\n{errors}.')
register_token_code('E02003', 'Global configuration validation failed with errors:\n{errors}.')
register_token_code('E02004', 'Initialisation data validation failed with errors:\n{errors}.')
register_token_code('E02005', 'Table {table} does not exist. It must be defined in the "tables" section.')
register_token_code('E02006', 'Database {database} does not exist. It must be defined in the "databases" section.')


class _ConfigValidator(BaseValidator):
    """Extend the base Cerberus validator class to include custom checks."""

    def _check_with_valid_genomic_library_table(self, field, value):
        """Validate the table referenced is defined."""
        if not value in self.document['tables']:
            self._error(field, str(text_token({'E02005': {'table': value}})))


    def _check_with_valid_default_database(self, field, value):
        """Validate the database referenced is defined."""
        if not value in self.document['databases']:
            self._error(field, str(text_token({'E02006': {'database': value}})))


    def _check_with_valid_database(self, field, value):
        """Validate the database referenced is defined."""
        if 'databases' in self.root_document and not value in self.root_document['databases']:
            self._error(field, str(text_token({'E02000': {'database': value}})))


    def _check_with_valid_file_folder(self, field, value):
        """Validate a table format file.

        If the 'format_file_folder' field is defined it is used as the path to
        the format file else it defaults to the 'formats' sub-folder of this
        source files folder.
        """
        self._isdir(field, value)


    def _check_with_valid_format_file(self, field, value):
        """Validate a table format file.

        If the 'format_file_folder' field is defined it is used as the path to
        the format file else it defaults to the 'formats' sub-folder of this
        source files folder.
        The table format file is checked to see if it is readable and if it is
        a decodable JSON format.
        Finally the table schema is validated.
        """
        abspath = join(self.document['format_file_folder'], value)
        for key, val in self._isjsonfile(field, abspath).items():
            if not 'meta' in val:
                self._error(field, str(text_token({'E02001': {'field': field}})))
            elif not entry_column_meta_validator(val['meta']):
                self._error(field, str(text_token({'E02002': {
                    'field': key,
                    'errors': pformat(entry_column_meta_validator.errors, width=180)
                }})))


    def _check_with_valid_data_files(self, field, value):
        """Validate table initialisation data.

        If the 'data_file_folder' field is defined it is used as the path to
        the data file else it defaults to the 'data' sub-folder of this
        source files folder.
        The table data file is checked to see if it is readable, if it is
        a decodable JSON format & valid.
        """
        _logger.debug("Loading validation schema {}.".format(self.document['format_file']))
        if self.document['format_file'] == "genomic_library_entry_format.json": validator = genomic_library_entry_validator
        elif self.document['format_file'] == "platform_info_entry_format.json": validator = platform_info_entry_validator
        elif self.document['format_file'] == "work_registry_entry_format.json": validator = work_registry_entry_validator
        elif self.document['format_file'] == "worker_registry_entry_format.json": validator = worker_registry_entry_validator
        elif self.document['format_file'] == "work_log_entry_format.json": validator = work_log_entry_validator
        else: validator = Validator
        schema_path = join(self.document['format_file_folder'], self.document['format_file'])
        with open(schema_path, "r") as schema_file:
            validator = validator(load(schema_file))

        for filename in value:
            abspath = join(self.document['data_file_folder'], filename)
            for datum in self._isjsonfile(field, abspath):
                if not validator.validate(datum):
                    self._error(field, str(text_token({'E02004': {'errors': pformat(validator.errors, width=180)}})))


    # pylint: disable=W0613, R0201
    # The parent class requires this function with a single argument and to get access
    # to the module scope.
    def _normalize_default_setter_set_format_file_folder(self, document):
        """Define the default 'format_file_folder'."""
        return join(dirname(__file__), 'formats')


    # pylint: disable=W0613, R0201
    # The parent class requires this function with a single argument and to get access
    # to the module scope.
    def _normalize_default_setter_set_data_file_folder(self, document):
        """Define the default 'data_file_folder'."""
        return join(dirname(__file__), 'data')


    # pylint: disable=W0613, R0201
    # The parent class requires this function with a single argument and to get access
    # to the module scope.
    def _normalize_default_setter_set_default_database(self, document):
        """Define the default database."""
        return self.root_document['default_database']


def set_config(new_config=None):
    """Set a new_config.

    The new_config is merged with the default configuration and validated.
    The resultant configuration is set regardless of validity.

    Args
    ----
    new_config(dict): A valid configuration dictionary.

    Returns
    -------
    The new configuration.
    """
    global _config #pylint: disable=C0103, W0603
    _config = {} if new_config is None else new_config
    return validate()


def validate():
    """Validate the global configuration.

    Validate the configuration file to be consistent with _CONFIG_FILE_FORMAT.
    If validation is successful the database table definition dictionaries are
    extended to include the loaded schemas.

    Returns
    -------
    (bool): True if the configuration is valid else False.
    """
    global _config #pylint: disable=C0103, W0603
    with open(join(dirname(__file__), _CONFIG_FORMAT_FILE), "r") as file_ptr:
        validator = _ConfigValidator(load(file_ptr))
    validator.allow_unknown = True
    _config = validator.normalized(_config)

    if not validator.validate(_config):
        global _errors #pylint: disable=C0103, W0603
        _errors = validator.errors
        _logger.error(str(text_token({'E02003': {'errors': pformat(validator.errors, width=180)}})))
        _logger.error('Configuration used:\n{}'.format(pformat(_config, width=180)))
        return False

    _errors = {}
    for value in _config['tables'].values():
        with open(join(value['format_file_folder'], value['format_file']), "r") as file_ptr:
            value['schema'] = load(file_ptr)
            for field in value['schema'].values():
                field['meta'] = entry_column_meta_validator.normalized(field['meta'])

    return True


def merge(dict_a, dict_b):
    """Merge nested dict_b into nested dict_a.

    If a key in dict_ b exists in dict_a it is over written in dict_a.

    Args
    ----
    dict_a (dict): Dictionary to be merged into.
    dict_b (dict): Dictionary to merge.

    Returns
    -------
    (dict): dict_b merged into dict_a
    """
    for key in dict_b:
        if key in dict_a and isinstance(dict_a[key], dict) and isinstance(dict_b[key], dict):
            merge(dict_a[key], dict_b[key])
        else:
            dict_a[key] = dict_b[key]
    return dict_a


def update_config(dict_c):
    """Update the global configuration with dict_c."""
    global _config #pylint: disable=C0103, W0603
    merge(_config, dict_c)
    return validate()


def save_config(config_file_path='config.json'):
    """Dump the current global configuration to file."""
    cfg = deepcopy(_config)
    for table in cfg['tables'].values(): del table['schema']
    with open(config_file_path, 'w') as file_ptr:
        dump(cfg, file_ptr, indent=4, sort_keys=True)


def get_config():
    """Return the current global configuration."""
    return _config


def get_errors():
    """If validation fails the error list will be non-empty."""
    return _errors


assert validate()
