"""Work is the definition of the evolutionary goals."""


from .config import get_config, update_config
from .database_table import database_table
from .work_registry_validator import work_registry_validator
from logging import getLogger


_logger = getLogger(__name__)


def register_work(work_config):
    """Register work."""
    work_config = validator.normalized(work_config)
    if not validator.validate(work_config):
        _logger.warning("Invalid work configuration: %s", validator.errors)
        return None
    work_registry = database_table(_logger, 'work_registry')
    work_registry.store([work_config])
    return work_config['signature']